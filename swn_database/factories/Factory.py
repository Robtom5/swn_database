#! /usr/bin/env python3
import abc


class Factory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(serializable_as_tuple: tuple):
        """Deserialize the class from a string"""
        raise NotImplementedError
