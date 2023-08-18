class RepresentationMixin:
    def __repr__(self) -> str:
        attributes = ", ".join(f"{key}={value}" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attributes})"
