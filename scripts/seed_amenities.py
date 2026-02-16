from app.database import SessionLocal
from app.models.amenity import Amenity

amenities = [
    ("Projector", False, None),
    ("Catering (per person)", True, 250.0),
    ("Stage Lighting", True, 1500.0),
    ("Sound System", True, 1200.0),
    ("Decor Package", True, 5000.0),
    ("Photo Booth", True, 3000.0),
    ("Valet Parking", True, 800.0),
    ("Air Conditioning", False, None),
    ("Bridal Room", False, None),
    ("Tables & Chairs", False, None),
    ("DJ Services", True, 4000.0),
    ("Live Band", True, 8000.0),
    ("Security Staff", True, 1500.0),
    ("Cleaning Service", True, 600.0),
    ("Wi-Fi Access", False, None)
]

if __name__ == '__main__':
    db = SessionLocal()
    added = 0
    for name, chargeable, price in amenities:
        exists = db.query(Amenity).filter(Amenity.amenity_name == name).first()
        if exists:
            print(f"Skipping existing amenity: {name}")
            continue
        a = Amenity(amenity_name=name, is_chargeable=chargeable, base_price=price)
        db.add(a)
        added += 1
    db.commit()
    print(f"Seed complete. Added {added} amenities.")
    total = db.query(Amenity).count()
    print(f"Total amenities in DB: {total}")
    db.close()
