from enum import Enum

class RARITY(Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    
    @classmethod
    def get_base_stars(cls, instance):
        if instance is cls.COMMON:
            return 3
        if instance is cls.RARE:
            return 4
        if instance is cls.EPIC:
            return 5
        if instance is cls.LEGENDARY:
            return 6

EXP_REQUIRED = [
    0, 100, 205, 316, 432, 553, 681, 815, 955, 1103, 1258, 1421, 1592, 1772, 1960,
    2158, 2366, 2585, 2814, 3054, 3307, 3572, 3851, 4144, 4451, 4773, 5112, 5467,
    5841, 6233, 6644, 7077, 7530, 8007, 8507, 9033, 9584, 10163, 10771, 11410,
    12080, 12784, 13524, 14300, 15115, 15971, 16869, 17812, 18803, 19843, 20935,
    22082, 23286, 24550, 25878, 27272, 28735, 30272, 31886, 33580, 35359, 37227,
    39188, 41247, 43410, 45680, 48064, 50567, 53196, 55956, 58853, 61896, 65091,
    68445, 71968, 75666, 79549, 83627, 87908, 92403, 97123, 102080, 107283,
    112748, 118485, 124509, 130835, 137476, 144450, 151773, 159461, 167534,
    176011, 184911, 194257, 204070, 214373, 225192, 236552, 248479, 261003,
    274153,
];