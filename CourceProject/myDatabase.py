from myModel import *
from peewee import *
import datetime

mainDatabase = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = mainDatabase


class Event(BaseModel):
    name = CharField()
    date = DateTimeField()


class Cook(BaseModel):
    name = CharField(unique=True)
    restaurant = CharField()


class Dish(BaseModel):
    name = CharField(unique=True)
    calorie = IntegerField()
    cook = ForeignKeyField(Cook)
    event = ForeignKeyField(Event)


class Drink(BaseModel):
    name = CharField(unique=True)
    count = IntegerField()
    event = ForeignKeyField(Event)


class Ingredient(BaseModel):
    name = CharField(unique=True)
    count = IntegerField()
    dish = ForeignKeyField(Dish)


class Recipe(BaseModel):
    author = CharField()
    dish = ForeignKeyField(Dish)


def initDatabase():
    ramsey = Cook.create(name="Гордон Рамзи", restaurant="Restaurant Gordon Ramsay")
    president_dinner = Event.create(name="обед с президентом",
                                    date=datetime.datetime(2020, 2, 1, 12, 0))
    scallop = Dish.create(name="гребешки", calorie=100, cook=ramsey, event=president_dinner)
    pasta = Dish.create(name="паста", calorie=300, cook=ramsey, event=president_dinner)
    roastbeef = Dish.create(name="ростбиф", calorie=200, cook=ramsey, event=president_dinner)
    mushroom_souse = Dish.create(name="грибной соус", calorie=100, cook=ramsey, event=president_dinner)
    champaign = Drink.create(name="Veuve Clicquot Ponsardin", count=25, event=president_dinner)
    raw_scallop = Ingredient.create(name="сырые гребешки", count=55, dish=scallop)
    recipe_scallop = Recipe.create(author="Гордон Рамзи", dish=scallop)
    raw_pasta = Ingredient.create(name="макароны", count=65, dish=pasta)
    spices = Ingredient.create(name="специи", count=45, dish=roastbeef)
    beef = Ingredient.create(name="говядина", count=45, dish=roastbeef)
    recipe_pasta = Recipe.create(author="Гордон Рамзи", dish=pasta)
    recipe_roastbeef = Recipe.create(author="Гордон Рамзи", dish=roastbeef)
    oliver = Cook.create(name="Джейми Оливер", restaurant="Jamies Italian")
    wedding = Event.create(name="свадьба", date=datetime.datetime(2019, 5, 3, 12, 0))
    mushroom_soup = Dish.create(name="грибной крем-суп", calorie=250, cook=oliver, event=wedding)
    mushrooms = Ingredient.create(name="грибы", count=35, dish=mushroom_soup)
    cream = Ingredient.create(name="сливки", count=35, dish=mushroom_soup)
    red_wine = Drink.create(name="Barolo", count=35, event=wedding)
    recipe_mushroom_soup = Recipe.create(author="Джейми Оливер", dish=mushroom_soup)


class MyDataBase:
    def __init__(self, name):
        mainDatabase.init(name)
        mainDatabase.connect()
        mainDatabase.create_tables(BaseModel.__subclasses__())
        try:
            initDatabase()
        except IntegrityError:
            pass

    def dishes(self):
        return [i.name for i in Dish.select()]

    def authors(self):
        return [i.author for i in Recipe.select(Recipe.author).distinct()]

    def maxDrinkCount(self):
        return Drink.select(fn.MAX(Drink.count)).scalar()

    def add(self, num, dish_name, name):
        try:
            dish = Dish.get(Dish.name == dish_name)
        except DoesNotExist:
            return

        Ingredient.create(name=name, count=num, dish=dish)

    def first(self, name):
        tmp = [(i.name, i.calorie) for i in
               Dish.select().join(Recipe).where(Recipe.author == name)]
        return MyModel(tmp, ['блюдо', 'калорийность'])

    def second(self, sub_str):
        tmp = [(i.cook.restaurant, i.cook.name, i.name) for i in
               Dish.select().join(Cook).where(Dish.name.contains(sub_str)).order_by(Cook.restaurant)]
        return MyModel(tmp, ['ресторан', 'повар', 'блюдо'])

    def third(self, num, date):
        tmp = [(i.dish.event.name, i.name, i.count) for i in
               Ingredient.select().join(Dish).join(Event).join(Drink).where(
                   (Drink.count < num) & (Event.date > date)).distinct()]
        return MyModel(tmp, ['событие', 'ингредиент', 'количество'])
