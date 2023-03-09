from flask import redirect, render_template, flash, url_for, request, session, current_app
from app import db, app, photos, search
from .models import Brand, Category, Product
from .forms import Addproducts
import secrets
import os


def brands():
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return brands


def categories():
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return categories


@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', products=products, brands=brands(), categories=categories())

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Product.query.msearch(searchword, fields=['name', 'desc'], limit=3)
    return render_template('products/result.html',  products=products, brands=brands(), categories=categories())


@app.route('/product/<int:id>')
def single_page(id):
    product = Product.query.get_or_404(id)
    return render_template('products/single_page.html', product=product, brands=brands(), categories=categories())

@app.route('/brands/<int:id>')
def getbrand(id):
    page = request.args.get('page', 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Product.query.filter_by(brand=get_b).order_by(
        Product.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', brand=brand, get_b=get_b, brands=brands(), categories=categories())


@app.route('/category/<int:id>')
def getcat(id):
    page = request.args.get('page', 1, type=int)
    cat = Category.query.filter_by(id=id).first_or_404()
    get_cat = Product.query.filter_by(category=cat).order_by(
        Product.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', get_cat=get_cat, cat=cat, brands=brands(), categories=categories())


@app.route('/add_brand', methods=['GET', 'POST'])
def add_brand():
    if 'email' not in session:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        get_brand = request.form.get('brand')
        brand = Brand(name=get_brand)
        db.session.add(brand)
        db.session.commit()
        flash(f'{get_brand} has been added', 'success')
        return redirect(url_for('add_brand'))
    return render_template('products/add_brand.html', brands='brands')


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(
            f'The brand was changed', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/add_brand.html', title='Update brand', brands='brands', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        flash(
            f"The brand {brand.name} was deleted from your database", "success")
        db.session.commit()
        return redirect(url_for('brands'))
    flash(
        f"The brand {brand.name} can't be  deleted from your database", "warning")
    return redirect(url_for('brands'))


@app.route('/add_cat', methods=['GET', 'POST'])
def add_cat():
    if 'email' not in session:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        get_cat = request.form.get('category')
        cat = Category(name=get_cat)
        db.session.add(cat)
        db.session.commit()
        flash(f'{get_cat} has been added', 'success')
        return redirect(url_for('add_cat'))
    return render_template('products/add_brand.html',)


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecat.name = category
        flash(
            f'The category {updatecat.name} was changed', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    category = updatecat.name
    return render_template('products/add_brand.html', title='Update category', categories='categories', updatecat=updatecat)


@app.route('/deletecat/<int:id>', methods=['GET', 'POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        flash(
            f"The brand {category.name} was deleted from your database", "success")
        db.session.commit()
        return redirect(url_for('brands'))
    flash(
        f"The brand {category.name} can't be  deleted from your database", "warning")
    return redirect(url_for('brands'))


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == 'POST' and 'image_1' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        color = form.color.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get(
            'image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get(
            'image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get(
            'image_3'), name=secrets.token_hex(10) + ".")
        product = Product(name=name, price=price, discount=discount, stock=stock, color=color,
                          desc=desc, category_id=category, brand_id=brand, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(product)
        flash(f'The product {name} was added!', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title='Add Products', form=form, brands=brands, categories=categories)


@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Product.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.color = form.color.data
        product.desc = form.description.data
        product.category_id = category
        product.brand_id = brand
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get(
                    'image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get(
                    'image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get(
                    'image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get(
                    'image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get(
                    'image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get(
                    'image_3'), name=secrets.token_hex(10) + ".")
        flash('The product was updated', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.color.data = product.color
    form.description.data = product.desc
    brand = product.brand.name
    category = product.category.name
    return render_template('products/addproduct.html', form=form, product=product, brands=brands, categories=categories)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(
            f'The product {product.name} was delete', 'success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product', 'success')
    return redirect(url_for('admin'))
