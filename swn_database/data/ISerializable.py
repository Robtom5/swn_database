#! /usr/bin/env python3
import abc


class ISerializable(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @abc.abstractmethod
    def deserialize(serializable_as_string: str):
        """Deserialize the class from a string"""
        raise NotImplementedError

    @abc.abstractmethod
    def serialize(self) -> str:
        """Serialize an instance of the class as a string"""
        raise NotImplementedError