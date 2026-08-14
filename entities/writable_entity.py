from dataclasses import dataclass
from typing import List, Dict



class WritableEntity():
    __writed: bool = False 

    def be_updated(self):
        self.__writed = False

    def be_writed(self):
        self.__writed = True

    @property
    def is_having_updates(self):
        return not self.__writed

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name != '_WritableEntity__writed':
            super().__setattr__('_WritableEntity__writed', False)

