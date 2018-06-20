from rest_framework import serializers


class ListToDictField(serializers.Field):
    """
    Represent a list of entities as a dictionary
    """
    def __init__(self, *args, **kwargs):
        self.child = kwargs.pop('child')
        self.key = kwargs.pop('key')

        assert self.child.source is None, (
            'The `source` argument is not meaningful when '
            'applied to a `child=` field. '
            'Remove `source=` from the field declaration.'
        )

        super(ListToDictField, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        list_data = self.child.to_representation(obj)
        data = {}

        for item in list_data:
            key_value = item.pop(self.key)
            data[str(key_value)] = item
        return data

    def to_internal_value(self, data):
        list_data = self.to_list_data(data)
        return self.child.run_validation(list_data)

    def to_list_data(self, data):
        list_data = []
        for key, value in data.items():
            list_data.append({
                self.key: key,
                **value,
            })
        return list_data
