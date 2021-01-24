# print("Hell", "Planet",'World')
#
# def average(*args):
#     print(type(args))
#     # print(type(*args))
#     print("the star args is : ", *args)
#     print("Args is {}".format(args))
#     mean = 0
#     for arg in args:
#         mean += arg
#     return mean / len(args)
#
#
# print(average(1, 2, 3, 4))


# def build_tuple(*args):
#     return args
#
#
# print("this function returns tuple: ", build_tuple(1, 2, 3, 4))

#
# def word_length(*args):
#     char_length = 0
#     for arg in args:
#         char_length += len(arg)
#     return char_length / len(args)
#
#
# print(word_length("saribeg", "seda"))

#
# def small(*args):
#     return min(args)
#
#
# print(small(20, 40, 80))


# def reverse(*args):
#     for arg in args:
#         print(arg[::-1], end=' ')
#
#
# reverse("Hello")


# def backward_words(*args, file=None):
#
#     for word in args[::-1]:
#         print(word[::-1], end=' ', file=file)

# def backward_words(*args, end="\n", **kwargs):
#     print(kwargs)
#     for word in args[::-1]:
#         print(word[::-1], end=end, **kwargs)
#
#
# with open("backwards.txt", 'w') as backwards:
#     # backward_words("hello", "planet", "earth", "take", "me", "to", "your", "leader", file=backwards, end='\n')
#     backward_words("hello", "planet", "earth", "take", "me", "to", "your", "leader")

# def backward_words(*args, **kwargs):
#     print(kwargs)
#     kwargs.pop('end', None)
#     for word in args[::-1]:
#         print(word[::-1], end=' ', **kwargs)


# with open("backwards.txt", 'w') as backwards:
# backward_words("hello", "planet", "earth", "take", "me", "to", "your", "leader", file=backwards, end='\n')
# backward_words("hello", "planet", "earth", "take", "me", "to", "your", "leader")

def backward_words(*args, **kwargs):
    end_character = kwargs.pop('end', '\n')
    sep_character = kwargs.pop('sep', ' ')
    print(sep_character.join(word[::-1] for word in args[::-1]), **kwargs)
    print(end=end_character)


print()
print("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n', sep='|')
backward_words("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n', sep='|')
print("=" * 10)