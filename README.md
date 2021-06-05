# Django Frozen Field

Django model custom field for storing a frozen snapshot of an object.

## Principles

* Behaves _like_ a `ForeignKey` but the data is detached from the related object
* Transparent to the client - it looks like the original object
* The frozen object cannot be edited
* The frozen object cannot be saved
* Works even if original model is updated or deleted

## Usage

A frozen field can be declared like a `ForeignKey`:

```python
class Profile(Model):

    address = FrozenObjectField(
        Address,              # The model being frozen - used in validation
        include=[],           # defaults to all non-related fields if not set
        exclude=["line_2"],   # remove from set of fields to serialize
        select_related=[]     # add related fields to serialization
        select_properties=["some_simple_property"]  # add model properties to serialization
    )
...

>>> profile.address = Address.objects.get(...)
>>> profile.address
"29 Acacia Avenue"
>>> profile.save()
>>> type(profile.address)
Address
# When fetched from the db, the property becomes a frozen instance
>>> profile.refresh_from_db()
>>> type(profile.address)
types.FrozenAddress
>>> profile.address.line_1
"29 Acacia Avenue"
>>> dataclasses.asdict(profile.address)
{
    "meta": {
        "pk": 1,
        "model": "Address",
        "frozen_at": "2021-06-04T18:10:30.549Z",
        "fields": {
            "id": "django.db.models.AutoField",
            "line_1": "django.db.models.CharField",
        },
        "properties": ["some_simple_property"]
    },
    "id": 1,
    "line_1": "29 Acacia Avenue",
    "some_simple_property": "hello"
}
>>> profile.address.id
1
>>> profile.address.id = 2
FrozenInstanceError: cannot assign to field 'id'
>>> profile.address.save()
AttributeError: 'FrozenAddress' object has no attribute 'save'
```

### Controlling serialization

By default only top-level attributes of an object are frozen - related objects
(`ForeignKey`, `OneToOneField`) are ignored. This is by design - as deep
serialization of recursive relationships can get very complex very quickly, and
a deep serialization of an object tree is not recommended. This library is
designed for the simple 'freezing' of basic data. The recommended pattern is to
flatten out the parts of the object tree that you wish to record. You can
control which top-level fields are included in the frozen data using the
`include` and `exclude` arguments. Note that these are mutually exclusive - by
default both are an empty list, which results in all top-level non-related
attributes being serialized. If `included` is not empty, then *only* the fields
in the list are serialized. If `excluded` is not empty then all fields *except*
those in the list are serialized.

That said, there is limited support for related object capture using the
`select_related` argument. This currently only supports one level of child
object serialization, but could be extended in the future to support Django ORM
`parent__child` style chaining of fields.

The `select_properties` argument can be used to add model properties (e.g.
methods decorated with `@property`) to the serialization. NB this currently does
no casting of the value when deserialized (as it doesn't know what the type is),
so if your property is a date, it will come back as a string (isoformat). If you
want it to return a `date` you will want to use converters.

The `converters` argument is used to override the default conversion of the JSON
back to something more appropriate. A typical use case would be the casting of a
property which has no default backing field to use. In this case you could use
the builtin Django `parse_date` function

```python
field = FrozenObjectField(
    Profile,
    include=[],
    exclude=[],
    select_related=[],
    select_properties=["date_registered"],
    converters={"date_registered": parse_date}
)
```

## How it works

The internal wrangling of a Django model to a JSON string is done using dynamic
dataclasses, created on the fly using the `dataclasses.make_dataclass` function.
The new dataclass contains one fixed property, `meta`, which is itself an
instance of a concrete dataclass, `FrozenObjectMeta`. This ensures that each
serialized blob contains enought original model field metadata to be able to
deserialize the JSONField back into something that resembles the original. This
is required because the process of serializing the data as JSON will convert
certain unsupported datatypes (e.g. `Decimal`, `float`, `date`, `datetime`,
`UUID`) to string equivalents, and in order to deserialize these values we need
to know what type the original value was. This is very similar to how Django's
own `django.core.serializers` work.

#### Running tests

The tests use `pytest` as the test runner. If you have installed the `poetry` evironment, you can run them using:

```
$ poetry run pytest
```
