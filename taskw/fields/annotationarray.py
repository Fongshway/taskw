from datetime import datetime

import six
from dateutil.parser import parse
from dateutil.tz import tzutc

from taskw.fields.array import ArrayField
from taskw.fields.base import DirtyableList
from taskw.utils import DATE_FORMAT


class Annotation(six.text_type):
    """ A special type of string that we'll use for storing annotations.

    This is, for all intents and purposes, really just a string, but
    it does allow us to store additional information if we have it -- in
    this application: the annotation's entry date.

    """
    def __new__(self, description, entry=None):
        return six.text_type.__new__(self, description)

    def __init__(self, description, entry=None):
        self._entry = entry
        super(Annotation, self).__init__()

    @property
    def entry(self):
        if self._entry:
            return parse(self._entry)
        return self._entry

    @entry.setter
    def entry(self, entry):
        self._entry = entry


class AnnotationArrayField(ArrayField):
    """ A special case of the ArrayField handling idiosyncrasies of Annotations

    Taskwarrior will currently return to you a dictionary of values --
    the annotation's date and description -- for each annotation, but
    given that we cannot create annotations with a date, let's instead
    return something that behaves like a string (but from which you can
    extract an entry date if one exists).

    """
    def deserialize(self, value):
        if not value:
            value = DirtyableList([])

        elements = []
        for annotation in value:
            if isinstance(annotation, dict):
                elements.append(
                    Annotation(
                        annotation['description'],
                        annotation['entry'],
                    )
                )
            else:
                elements.append(Annotation(annotation))

        return super(AnnotationArrayField, self).deserialize(elements)

    def serialize(self, annotations):
        if not annotations:
            annotations = []

        for annotation in annotations:
            if not annotation.entry:
                annotation.entry = datetime.now().replace(tzinfo=tzutc()).strftime(DATE_FORMAT)

        return super(AnnotationArrayField, self).serialize(
            [
                {
                    'entry': annotation.entry.strftime(DATE_FORMAT),
                    'description': six.text_type(annotation)
                } for annotation in annotations
            ]

        )
