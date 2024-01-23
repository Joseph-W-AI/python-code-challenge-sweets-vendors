from app import app, db
from models import Vendor, Sweet, VendorSweet

with app.app_context():
    db.drop_all()
    db.create_all()

    # Vendors
    insomnia = Vendor(name='Insomnia Cookies')
    cookies_cream = Vendor(name="Cookies Cream")

    db.session.add(insomnia)
    db.session.add(cookies_cream)

    # Sweets 
    choc_chip = Sweet(name='Chocolate Chip Cookie')
    brownie = Sweet(name='Brownie')

    db.session.add(choc_chip)
    db.session.add(brownie)

    # VendorSweets
    vs1 = VendorSweet(price=200, vendor=insomnia, sweet=choc_chip)
    vs2 = VendorSweet(price=300, vendor=insomnia, sweet=brownie)

    db.session.add(vs1)
    db.session.add(vs2)

    db.session.commit()
