class Dog:
    def bark(self):
        return 'Woof!'

    def pet(self):
        return self.bark()

# Dog is being passed to the owner
class Owner:
    def __init__(self, dog: Dog):
        self.dog = dog

    def pet_dog(self):
        # Call to instance method!
        self.dog.pet()

# Dog is being created in the owner
class Owner2:
    def __init__(self):
        self.dog = Dog()

    def pet_dog(self):
        # Call to instance method!
        self.dog.pet()


# Function calling a defintion
def pet_dog():
    dog = Dog()
    dog.pet()


# Dog is passed as an argument
def pet_dog(dog: Dog):
    dog.pet()


# Calls outside functions/classes
dog = Dog()
dog.bark()
dog.pet()