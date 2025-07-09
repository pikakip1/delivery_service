import enum


class ParcelType(str, enum.Enum):
    DOCUMENT = "document"
    PACKAGE = "package"
    LETTER = "letter"