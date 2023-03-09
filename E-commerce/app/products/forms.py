from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import IntegerField, StringField, BooleanField, TextAreaField, validators, Form, DecimalField


class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount')
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    color = TextAreaField('Colors', [validators.DataRequired()])
    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'gif'])])
