from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List, Union
from fastapi.middleware.cors import CORSMiddleware
from db import session, ENGINE
import pandas as pd
import pandasql as ps
import sqlalchemy
from typing import Optional

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World!!!!"}


@app.get("/ingest_sample_data")
def ingest_sample_data():
    # cities
    df_zips = pd.read_csv("sample_data/cities/uszips.csv")
    df_zips = ps.sqldf(
        """
        SELECT
            zip AS postal_code,
            city,
            lng AS longitude,
            lat AS latitude,
            state_id AS state
        FROM df_zips
        """
    )

    try:
        df_zips.to_sql("city_info", con=ENGINE, if_exists="append", index=False)
        # commit changes
        session.commit()

    except sqlalchemy.exc.IntegrityError:
        print("Data already exists in the database")

    # household
    df = pd.read_csv("sample_data/Household.tsv", sep="\t")
    # run sql against the df
    test = ps.sqldf(
        """
            SELECT
            df.postal_code
            FROM df
            LEFT JOIN df_zips ON df_zips.postal_code = df.postal_code
            WHERE city IS NULL
        """
    )

    df_house = ps.sqldf(
        """
            SELECT
                email,
                footage AS square_footage,
                num_occupants AS number_of_occupants,
                bedroom_count AS number_of_bedrooms,
                household_type,
                postal_code
            FROM df
            WHERE postal_code NOT IN (SELECT postal_code FROM test)
        """
    )

    # push to db
    try:
        df_house.to_sql("household", con=ENGINE, if_exists="append", index=False)
    except sqlalchemy.exc.IntegrityError:
        print("Data already exists in database, skipping")
    # run sql against the df
    df_phone = ps.sqldf(
        """
            SELECT
                phone_number,
                area_code,
                phone_type,
                email
            FROM df
            WHERE postal_code NOT IN (SELECT postal_code FROM test)
            AND phone_number IS NOT NULL
        """
    )

    # push to db
    try:
        df_phone.to_sql("phone_info", con=ENGINE, if_exists="append", index=False)
    except sqlalchemy.exc.IntegrityError:
        print("Data already exists in database, skipping")

    df_manufacturers = pd.read_csv("sample_data/Manufacturer.tsv", sep="\t")
    df_manufacturers.reset_index(inplace=True)
    df_manufacturers["id"] = df_manufacturers["index"] + 1
    df_manufacturers = ps.sqldf(
        """
            SELECT
            id,
            manufacturer_name
            FROM df_manufacturers
        """
    )

    # push to db
    try:
        df_manufacturers.to_sql(
            "manufacturer", con=ENGINE, if_exists="append", index=False
        )
    except sqlalchemy.exc.IntegrityError:
        print("Data already exists in database, skipping")

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(
            {"message": "Data successfully ingested or skipped due to existing data"}
        ),
    )


@app.post("/do_all")
def do_all():
    """A utlity function to simulate a full data pipeline. Only runnable once.
    Details:
        Household
            - email: sample@email.com
            - postal_code: 601
            - Home type: apartment
            - square footage: 1000
            - Number of occupants: 2
            - Number of bedrooms: 2

        Phone
            - Area: 134
            - phone_number: 4375345
            - Type: Mobile

        Bathrooms
            Half Bathroom
                - Number of sinks: 1
                - Number of commodes: 2
                - Number of bidets: 1
                - Name: sample_half_bath
            Full Bathroom
                1
                    - Number of sinks: 3
                    - Number of commodes: 4
                    - Number of bidets: 2
                    - Number of bathtubs: 2
                    - Number of showers: 1
                    - Number of tub showers: 1
                    - Primary: true
                2
                    - Number of sinks: 2
                    - Number of commodes: 3
                    - Number of bidets: 1
                    - Number of bathtubs: 1
                    - Number of showers: 0
                    - Number of tub showers: 0
                    - Primary: false
        Appliances
            Dryer
                - Manufacturer: 1
                - Model: sample_dryer
                - Heat source: electric
            Fridge
                - Manufacturer: 2
                - Model: sample_fridge
                - Fridge type: chest freezer
            Washer
                - Manufacturer: 3
                - Model: sample_washer
                - Load type: front
            TV
                - Manufacturer: 4
                - Model: sample_tv
                - display_type: LCD
                - max resolution: 1080p
                - display_size: 32
            Cooker
                Cooktop
                    - Manufacturer: 5
                    - Model: sample_cooktop
                    - heat_source: electric
                Oven
                    - Manufacturer: 5
                    - Model: sample_oven
                    - Oven type: electric
                    - heat_source: electric, gas
    """

    # ingest data
    ingest_sample_data()

    # validate email
    validate_email("sample@email.com")

    # validate postal code
    validate_postal_code(601)

    # validate phone
    validate_phone_number(134, 4375345)

    # Insert into household
    insert_household(
        "sample@email.com",
        1000,
        2,
        2,
        "apartment",
        601,
    )

    # Insert into phone
    insert_phone_number(
        134,
        4375345,
        "Mobile",
        "sample@email.com",
    )

    # Insert into half bath
    insert_half_bathroom(
        "sample@email.com",
        1,
        2,
        1,
        "sample_half_bath",
    )

    # Insert into full bath
    insert_full_bathroom(
        "sample@email.com",
        3,
        4,
        2,
        2,
        1,
        1,
        True,
    )

    insert_full_bathroom(
        "sample@email.com",
        2,
        3,
        1,
        1,
        0,
        0,
        False,
    )

    # Insert dryer
    insert_appliance(
        "sample_dryer",
        1,
        "sample@email.com",
        "Dryer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample@email.com'"
    ).fetchone()[0]

    insert_dryer(
        "electric",
        appliance_number,
        "sample@email.com",
    )

    # Insert fridge
    insert_appliance(
        "sample_fridge",
        2,
        "sample@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "chest freezer",
        appliance_number,
        "sample@email.com",
    )

    # Insert washer
    insert_appliance(
        "sample_washer",
        3,
        "sample@email.com",
        "Washer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample@email.com'"
    ).fetchone()[0]

    insert_washer(
        "front",
        appliance_number,
        "sample@email.com",
    )

    # Insert TV
    insert_appliance(
        "sample_tv",
        4,
        "sample@email.com",
        "TV",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample@email.com'"
    ).fetchone()[0]

    insert_tv(
        "LCD",
        32.0,
        "1080p",
        appliance_number,
        "sample@email.com",
    )

    # Insert cooker
    insert_appliance(
        "sample_cooktop",
        5,
        "sample@email.com",
        "Cooker",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample@email.com'",
    ).fetchone()[0]

    insert_cooktop(
        "electric",
        appliance_number,
        "sample@email.com",
    )

    insert_appliance("sample_oven", 5, "sample@email.com", "Oven")

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample@email.com'",
    ).fetchone()[0]

    insert_oven(
        "electric",
        appliance_number,
        "sample@email.com",
    )

    insert_oven_heat_source(
        "electric,gas",
        appliance_number,
        "sample@email.com",
    )

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({"message": "Data successfully ingested"}),
    )


@app.post("/do_all_times_eight")
def do_all_times_eight():
    #####First
    # ingest data
    ingest_sample_data()

    # validate email
    validate_email("sample1@email.com")

    # validate postal code
    validate_postal_code(90403)

    # validate phone
    validate_phone_number(111, 1111111)

    # Insert into household
    insert_household(
        "sample1@email.com",
        1000,
        2,
        2,
        "apartment",
        90403,
    )

    # Insert into phone
    insert_phone_number(
        111,
        1111111,
        "Mobile",
        "sample1@email.com",
    )

    # Insert into half bath
    insert_half_bathroom(
        "sample1@email.com",
        1,
        2,
        1,
        "sample_half_bath",
    )

    # Insert into full bath
    insert_full_bathroom(
        "sample1@email.com",
        3,
        4,
        2,
        2,
        1,
        1,
        True,
    )

    insert_full_bathroom(
        "sample1@email.com",
        2,
        3,
        1,
        1,
        0,
        0,
        False,
    )

    # Insert dryer
    insert_appliance(
        "sample_dryer",
        1,
        "sample1@email.com",
        "Dryer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample1@email.com'"
    ).fetchone()[0]

    insert_dryer(
        "electric",
        appliance_number,
        "sample1@email.com",
    )

    # Insert fridge
    insert_appliance(
        "sample_fridge",
        2,
        "sample1@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample1@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "chest freezer",
        appliance_number,
        "sample1@email.com",
    )

    # Insert washer
    insert_appliance(
        "sample_washer",
        3,
        "sample1@email.com",
        "Washer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample1@email.com'"
    ).fetchone()[0]

    insert_washer(
        "front",
        appliance_number,
        "sample1@email.com",
    )

    # Insert TV
    insert_appliance(
        "sample_tv",
        4,
        "sample1@email.com",
        "TV",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample1@email.com'"
    ).fetchone()[0]

    insert_tv(
        "LCD",
        32.0,
        "1080p",
        appliance_number,
        "sample1@email.com",
    )

    # Insert cooker
    insert_appliance(
        "sample_cooktop",
        5,
        "sample1@email.com",
        "Cooker",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample1@email.com'",
    ).fetchone()[0]

    insert_cooktop(
        "electric",
        appliance_number,
        "sample1@email.com",
    )

    insert_appliance("sample_oven", 5, "sample1@email.com", "Oven")

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample1@email.com'",
    ).fetchone()[0]

    insert_oven(
        "electric",
        appliance_number,
        "sample1@email.com",
    )

    insert_oven_heat_source(
        "electric,gas",
        appliance_number,
        "sample1@email.com",
    )

    #####Second
    # ingest data
    ingest_sample_data()

    # validate email
    validate_email("sample2@email.com")

    # validate postal code
    validate_postal_code(90403)

    # validate phone
    validate_phone_number(222, 2222222)

    # Insert into household
    insert_household(
        "sample2@email.com",
        1000,
        2,
        2,
        "apartment",
        90403,
    )

    # Insert into phone
    insert_phone_number(
        222,
        2222222,
        "Mobile",
        "sample2@email.com",
    )

    # Insert into half bath
    insert_half_bathroom(
        "sample2@email.com",
        1,
        2,
        1,
        "sample_half_bath",
    )

    # Insert into full bath
    insert_full_bathroom(
        "sample2@email.com",
        3,
        4,
        2,
        2,
        1,
        1,
        True,
    )

    insert_full_bathroom(
        "sample2@email.com",
        2,
        3,
        1,
        1,
        0,
        0,
        False,
    )

    # Insert dryer
    insert_appliance(
        "sample_dryer",
        1,
        "sample2@email.com",
        "Dryer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample2@email.com'"
    ).fetchone()[0]

    insert_dryer(
        "electric",
        appliance_number,
        "sample2@email.com",
    )

    # Insert fridge
    insert_appliance(
        "sample_fridge",
        2,
        "sample2@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample2@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "chest freezer",
        appliance_number,
        "sample2@email.com",
    )

    # Insert washer
    insert_appliance(
        "sample_washer",
        3,
        "sample2@email.com",
        "Washer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample2@email.com'"
    ).fetchone()[0]

    insert_washer(
        "front",
        appliance_number,
        "sample2@email.com",
    )

    # Insert TV
    insert_appliance(
        "sample_tv",
        4,
        "sample2@email.com",
        "TV",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample2@email.com'"
    ).fetchone()[0]

    insert_tv(
        "LCD",
        64,
        "1080p",
        appliance_number,
        "sample2@email.com",
    )

    # Insert cooker
    insert_appliance(
        "sample_cooktop",
        5,
        "sample2@email.com",
        "Cooker",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample2@email.com'",
    ).fetchone()[0]

    insert_cooktop(
        "electric",
        appliance_number,
        "sample2@email.com",
    )

    insert_appliance("sample_oven", 5, "sample2@email.com", "Oven")

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample2@email.com'",
    ).fetchone()[0]

    insert_oven(
        "electric",
        appliance_number,
        "sample2@email.com",
    )
    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample2@email.com'"
    ).fetchone()[0]

    insert_oven_heat_source(
        "gas",
        appliance_number,
        "sample2@email.com",
    )

    insert_appliance(
        "sample_fridge",
        8,
        "sample2@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample2@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "upright",
        appliance_number,
        "sample2@email.com",
    )
    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample2@email.com'"
    ).fetchone()[0]

    insert_appliance(
        "sample_fridge",
        9,
        "sample2@email.com",
        "Fridge",
    )
    #####Third
    # ingest data
    ingest_sample_data()

    # validate email
    validate_email("sample3@email.com")

    # validate postal code
    validate_postal_code(30083)

    # validate phone
    validate_phone_number(333, 3333333)

    # Insert into household
    insert_household(
        "sample3@email.com",
        1000,
        2,
        2,
        "apartment",
        30083,
    )

    # Insert into phone
    insert_phone_number(
        333,
        3333333,
        "Mobile",
        "sample3@email.com",
    )

    # Insert into half bath
    insert_half_bathroom(
        "sample3@email.com",
        1,
        2,
        1,
        "sample_half_bath",
    )

    # Insert into full bath
    insert_full_bathroom(
        "sample3@email.com",
        3,
        4,
        2,
        2,
        1,
        1,
        True,
    )

    insert_full_bathroom(
        "sample3@email.com",
        2,
        3,
        1,
        1,
        0,
        0,
        False,
    )

    # Insert dryer
    insert_appliance(
        "sample_dryer",
        1,
        "sample3@email.com",
        "Dryer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample3@email.com'"
    ).fetchone()[0]

    insert_dryer(
        "electric",
        appliance_number,
        "sample3@email.com",
    )

    # Insert fridge
    insert_appliance(
        "sample_fridge",
        2,
        "sample3@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample3@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "chest freezer",
        appliance_number,
        "sample3@email.com",
    )

    # Insert washer
    insert_appliance(
        "sample_washer",
        3,
        "sample3@email.com",
        "Washer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample3@email.com'"
    ).fetchone()[0]

    insert_washer(
        "front",
        appliance_number,
        "sample3@email.com",
    )

    # Insert TV
    insert_appliance(
        "sample_tv",
        4,
        "sample3@email.com",
        "TV",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample3@email.com'"
    ).fetchone()[0]

    insert_tv(
        "LCD",
        12,
        "1080p",
        appliance_number,
        "sample3@email.com",
    )

    # Insert cooker
    insert_appliance(
        "sample_cooktop",
        5,
        "sample3@email.com",
        "Cooker",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample3@email.com'",
    ).fetchone()[0]

    insert_cooktop(
        "electric",
        appliance_number,
        "sample3@email.com",
    )

    insert_appliance("sample_oven", 5, "sample3@email.com", "Oven")

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample3@email.com'",
    ).fetchone()[0]

    insert_oven(
        "electric",
        appliance_number,
        "sample3@email.com",
    )

    insert_oven_heat_source(
        "electric,gas",
        appliance_number,
        "sample3@email.com",
    )
    ##Fourth Person
    # ingest data
    ingest_sample_data()

    # validate email
    validate_email("sample4@email.com")

    # validate postal code
    validate_postal_code(90403)

    # validate phone
    validate_phone_number(444, 4444444)

    # Insert into household
    insert_household(
        "sample4@email.com",
        1000,
        2,
        2,
        "apartment",
        90403,
    )

    # Insert into phone
    insert_phone_number(
        444,
        4444444,
        "Mobile",
        "sample4@email.com",
    )

    # Insert into half bath
    insert_half_bathroom(
        "sample4@email.com",
        1,
        2,
        1,
        "sample_half_bath",
    )

    # Insert into full bath
    insert_full_bathroom(
        "sample4@email.com",
        3,
        4,
        2,
        2,
        1,
        1,
        True,
    )

    insert_full_bathroom(
        "sample4@email.com",
        2,
        3,
        1,
        1,
        0,
        0,
        False,
    )

    # Insert dryer
    insert_appliance(
        "sample_dryer",
        1,
        "sample4@email.com",
        "Dryer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample4@email.com'"
    ).fetchone()[0]

    insert_dryer(
        "electric",
        appliance_number,
        "sample4@email.com",
    )

    # Insert fridge
    insert_appliance(
        "sample_fridge",
        2,
        "sample4@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample4@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "chest freezer",
        appliance_number,
        "sample4@email.com",
    )

    # Insert washer
    insert_appliance(
        "sample_washer",
        3,
        "sample4@email.com",
        "Washer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample4@email.com'"
    ).fetchone()[0]

    insert_washer(
        "front",
        appliance_number,
        "sample4@email.com",
    )

    # Insert TV
    insert_appliance(
        "sample_tv",
        4,
        "sample4@email.com",
        "TV",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample4@email.com'"
    ).fetchone()[0]

    insert_tv(
        "LCD",
        64,
        "1080p",
        appliance_number,
        "sample4@email.com",
    )

    # Insert cooker
    insert_appliance(
        "sample_cooktop",
        5,
        "sample4@email.com",
        "Cooker",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample4@email.com'",
    ).fetchone()[0]

    insert_cooktop(
        "electric",
        appliance_number,
        "sample4@email.com",
    )

    insert_appliance("sample_oven", 5, "sample4@email.com", "Oven")

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample4@email.com'",
    ).fetchone()[0]

    insert_oven(
        "electric",
        appliance_number,
        "sample4@email.com",
    )
    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample4@email.com'"
    ).fetchone()[0]

    insert_oven_heat_source(
        "electric,gas",
        appliance_number,
        "sample4@email.com",
    )

    insert_appliance(
        "sample_fridge",
        8,
        "sample4@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample4@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "upright",
        appliance_number,
        "sample4@email.com",
    )
    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample4@email.com'"
    ).fetchone()[0]

    insert_appliance(
        "sample_fridge",
        9,
        "sample4@email.com",
        "Fridge",
    )
    #####Fifth
    # ingest data
    ingest_sample_data()

    # validate email
    validate_email("sample5@email.com")

    # validate postal code
    validate_postal_code(30143)

    # validate phone
    validate_phone_number(555, 5555555)

    # Insert into household
    insert_household(
        "sample5@email.com",
        1000,
        2,
        2,
        "apartment",
        30143,
    )

    # Insert into phone
    insert_phone_number(
        555,
        5555555,
        "Mobile",
        "sample5@email.com",
    )

    # Insert into half bath
    insert_half_bathroom(
        "sample5@email.com",
        1,
        2,
        1,
        "sample_half_bath",
    )

    # Insert into full bath
    insert_full_bathroom(
        "sample5@email.com",
        3,
        4,
        2,
        2,
        1,
        1,
        True,
    )

    insert_full_bathroom(
        "sample5@email.com",
        2,
        3,
        1,
        1,
        0,
        0,
        False,
    )

    # Insert fridge
    insert_appliance(
        "sample_fridge",
        2,
        "sample5@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample5@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "chest freezer",
        appliance_number,
        "sample5@email.com",
    )

    # Insert washer
    insert_appliance(
        "sample_washer",
        3,
        "sample5@email.com",
        "Washer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample5@email.com'"
    ).fetchone()[0]

    insert_washer(
        "front",
        appliance_number,
        "sample5@email.com",
    )

    # Insert TV
    insert_appliance(
        "sample_tv",
        4,
        "sample5@email.com",
        "TV",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample5@email.com'"
    ).fetchone()[0]

    insert_tv(
        "LCD",
        24.0,
        "1080p",
        appliance_number,
        "sample5@email.com",
    )

    # Insert cooker
    insert_appliance(
        "sample_cooktop",
        5,
        "sample5@email.com",
        "Cooker",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample5@email.com'",
    ).fetchone()[0]

    insert_cooktop(
        "electric",
        appliance_number,
        "sample5@email.com",
    )

    insert_appliance("sample_oven", 5, "sample5@email.com", "Oven")

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample5@email.com'",
    ).fetchone()[0]

    insert_oven(
        "electric",
        appliance_number,
        "sample5@email.com",
    )

    insert_oven_heat_source(
        "electric",
        appliance_number,
        "sample5@email.com",
    )
    ##Sixth Person
    # ingest data
    ingest_sample_data()

    # validate email
    validate_email("sample6@email.com")

    # validate postal code
    validate_postal_code(30803)

    # validate phone
    validate_phone_number(666, 6666666)

    # Insert into household
    insert_household(
        "sample6@email.com",
        1000,
        2,
        2,
        "apartment",
        30803,
    )

    # Insert into phone
    insert_phone_number(
        666,
        6666666,
        "Mobile",
        "sample6@email.com",
    )

    # Insert into half bath
    insert_half_bathroom(
        "sample6@email.com",
        1,
        2,
        1,
        "sample_half_bath",
    )

    # Insert into full bath
    insert_full_bathroom(
        "sample6@email.com",
        3,
        4,
        2,
        2,
        1,
        1,
        True,
    )

    insert_full_bathroom(
        "sample6@email.com",
        2,
        3,
        1,
        1,
        0,
        0,
        False,
    )

    # Insert fridge
    insert_appliance(
        "sample_fridge",
        2,
        "sample6@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample6@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "chest freezer",
        appliance_number,
        "sample6@email.com",
    )

    # Insert washer
    insert_appliance(
        "sample_washer",
        3,
        "sample6@email.com",
        "Washer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample6@email.com'"
    ).fetchone()[0]

    insert_washer(
        "front",
        appliance_number,
        "sample6@email.com",
    )

    # Insert TV
    insert_appliance(
        "sample_tv",
        4,
        "sample6@email.com",
        "TV",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample6@email.com'"
    ).fetchone()[0]

    insert_tv(
        "LCD",
        64,
        "1080p",
        appliance_number,
        "sample6@email.com",
    )

    # Insert cooker
    insert_appliance(
        "sample_cooktop",
        5,
        "sample6@email.com",
        "Cooker",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample6@email.com'",
    ).fetchone()[0]

    insert_cooktop(
        "electric",
        appliance_number,
        "sample6@email.com",
    )

    insert_appliance("sample_oven", 5, "sample6@email.com", "Oven")

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample6@email.com'",
    ).fetchone()[0]

    insert_oven(
        "electric",
        appliance_number,
        "sample6@email.com",
    )
    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample6@email.com'"
    ).fetchone()[0]

    insert_oven_heat_source(
        "electric",
        appliance_number,
        "sample6@email.com",
    )

    insert_appliance(
        "sample_fridge",
        8,
        "sample6@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample6@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "upright",
        appliance_number,
        "sample6@email.com",
    )
    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample6@email.com'"
    ).fetchone()[0]

    insert_appliance(
        "sample_fridge",
        9,
        "sample6@email.com",
        "Fridge",
    )
    #####Seventh
    # ingest data
    ingest_sample_data()

    # validate email
    validate_email("sample7@email.com")

    # validate postal code
    validate_postal_code(610)

    # validate phone
    validate_phone_number(777, 7777777)

    # Insert into household
    insert_household(
        "sample7@email.com",
        1000,
        2,
        2,
        "apartment",
        610,
    )

    # Insert into phone
    insert_phone_number(
        777,
        7777777,
        "Mobile",
        "sample7@email.com",
    )

    # Insert into half bath
    insert_half_bathroom(
        "sample7@email.com",
        1,
        2,
        1,
        "sample_half_bath",
    )

    # Insert into full bath
    insert_full_bathroom(
        "sample7@email.com",
        3,
        4,
        2,
        2,
        1,
        1,
        True,
    )

    insert_full_bathroom(
        "sample7@email.com",
        2,
        3,
        1,
        1,
        0,
        0,
        False,
    )

    # Insert fridge
    insert_appliance(
        "sample_fridge",
        2,
        "sample7@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample7@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "side",
        appliance_number,
        "sample7@email.com",
    )

    # Insert washer
    insert_appliance(
        "sample_washer",
        3,
        "sample7@email.com",
        "Washer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample7@email.com'"
    ).fetchone()[0]

    insert_washer(
        "front",
        appliance_number,
        "sample7@email.com",
    )

    # Insert TV
    insert_appliance(
        "sample_tv",
        4,
        "sample7@email.com",
        "TV",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample7@email.com'"
    ).fetchone()[0]

    insert_tv(
        "LCD",
        19.0,
        "1080p",
        appliance_number,
        "sample7@email.com",
    )

    # Insert cooker
    insert_appliance(
        "sample_cooktop",
        5,
        "sample7@email.com",
        "Cooker",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample7@email.com'",
    ).fetchone()[0]

    insert_cooktop(
        "electric",
        appliance_number,
        "sample7@email.com",
    )

    insert_appliance("sample_oven", 5, "sample7@email.com", "Oven")

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample7@email.com'",
    ).fetchone()[0]

    insert_oven(
        "electric",
        appliance_number,
        "sample7@email.com",
    )

    insert_oven_heat_source(
        "gas",
        appliance_number,
        "sample7@email.com",
    )
    ##Eighth Person
    # ingest data
    ingest_sample_data()

    # validate email
    validate_email("sample8@email.com")

    # validate postal code
    validate_postal_code(603)

    # validate phone
    validate_phone_number(888, 8888888)

    # Insert into household
    insert_household(
        "sample8@email.com",
        1000,
        2,
        2,
        "apartment",
        603,
    )

    # Insert into phone
    insert_phone_number(
        888,
        8888888,
        "Mobile",
        "sample8@email.com",
    )

    # Insert into half bath
    insert_half_bathroom(
        "sample8@email.com",
        1,
        2,
        1,
        "sample_half_bath",
    )

    # Insert into full bath
    insert_full_bathroom(
        "sample8@email.com",
        3,
        4,
        2,
        2,
        1,
        1,
        True,
    )

    insert_full_bathroom(
        "sample8@email.com",
        2,
        3,
        1,
        1,
        0,
        0,
        False,
    )

    # Insert fridge
    insert_appliance(
        "sample_fridge",
        2,
        "sample8@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample8@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "french",
        appliance_number,
        "sample8@email.com",
    )

    # Insert washer
    insert_appliance(
        "sample_washer",
        3,
        "sample8@email.com",
        "Washer",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample8@email.com'"
    ).fetchone()[0]

    insert_washer(
        "front",
        appliance_number,
        "sample8@email.com",
    )

    # Insert TV
    insert_appliance(
        "sample_tv",
        4,
        "sample8@email.com",
        "TV",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample8@email.com'"
    ).fetchone()[0]

    insert_tv(
        "LCD",
        19,
        "1080p",
        appliance_number,
        "sample8@email.com",
    )

    # Insert cooker
    insert_appliance(
        "sample_cooktop",
        5,
        "sample8@email.com",
        "Cooker",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample8@email.com'",
    ).fetchone()[0]

    insert_cooktop(
        "electric",
        appliance_number,
        "sample8@email.com",
    )

    insert_appliance("sample_oven", 5, "sample8@email.com", "Oven")

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample8@email.com'",
    ).fetchone()[0]

    insert_oven(
        "electric",
        appliance_number,
        "sample8@email.com",
    )
    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample8@email.com'"
    ).fetchone()[0]

    insert_oven_heat_source(
        "gas",
        appliance_number,
        "sample8@email.com",
    )

    insert_appliance(
        "sample_fridge",
        8,
        "sample8@email.com",
        "Fridge",
    )

    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample8@email.com'"
    ).fetchone()[0]

    insert_fridge(
        "side",
        appliance_number,
        "sample8@email.com",
    )
    appliance_number = session.execute(
        "SELECT MAX(appliance_number) FROM appliance WHERE email = 'sample8@email.com'"
    ).fetchone()[0]

    insert_appliance(
        "sample_fridge",
        9,
        "sample8@email.com",
        "Fridge",
    )
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({"message": "Data successfully ingested"}),
    )


@app.post("/validate_email")
def validate_email(email: str):
    user = session.execute(
        "SELECT * FROM household WHERE email = :email", {"email": email}
    ).fetchone()
    if user:
        return JSONResponse(content=jsonable_encoder({"valid": False}))
    else:
        return JSONResponse(content=jsonable_encoder({"valid": True}))


@app.post("/validate_postal_code")
def validate_postal_code(postal_code: int):
    city = session.execute(
        "SELECT postal_code, city, state"
        " FROM city_info WHERE postal_code = :postal_code",
        {"postal_code": postal_code},
    ).fetchone()

    if not city:
        return JSONResponse(content=jsonable_encoder({"valid": False}))

    return JSONResponse(content=jsonable_encoder(city))


@app.post("/validate_phone_number")
def validate_phone_number(area_code: int, seven_digits: int):
    if len(str(seven_digits)) != 7:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )

    if len(str(area_code)) != 3:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {"success": False, "message": "Invalid area code"}
            ),
        )

    phone = session.execute(
        "SELECT phone_number"
        " FROM phone_info WHERE area_code = :area_code"
        " AND phone_number = :seven_digits",
        {
            "area_code": area_code,
            "seven_digits": seven_digits,
        },
    )

    if phone.one_or_none():
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Phone number already exists",
                }
            ),
        )

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.post("/insert_phone_number")
def insert_phone_number(
    area_code: int,
    seven_digits: int,
    phone_type: str,
    email: str,
):
    session.execute(
        "INSERT INTO phone_info"
        " VALUES (:seven_digits, :area_code, :phone_type, :email)",
        {
            "area_code": area_code,
            "seven_digits": seven_digits,
            "phone_type": phone_type,
            "email": email,
        },
    )

    session.commit()

    phone = session.execute(
        "SELECT * FROM phone_info"
        " WHERE area_code = :area_code"
        " AND phone_number = :seven_digits",
        {
            "area_code": area_code,
            "seven_digits": seven_digits,
        },
    ).fetchone()

    return JSONResponse(content=jsonable_encoder(phone))


@app.post("/insert_household")
def insert_household(
    email: str,
    square_footage: int,
    number_of_occupants: int,
    number_of_bedrooms: int,
    household_type: str,
    postal_code: int,
):
    if square_footage <= 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    if number_of_occupants <= 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    if number_of_bedrooms < 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    session.execute(
        "INSERT INTO household"
        " VALUES (:email, :square_footage, :number_of_occupants, :number_of_bedrooms, :household_type, :postal_code)",
        {
            "email": email,
            "square_footage": square_footage,
            "number_of_occupants": number_of_occupants,
            "number_of_bedrooms": number_of_bedrooms,
            "household_type": household_type,
            "postal_code": postal_code,
        },
    )

    session.commit()

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.post("/insert_half_bathroom")
def insert_half_bathroom(
    email: str,
    number_of_sinks: int,
    number_of_commodes: int,
    number_of_bidets: int,
    half_bath_name: Optional[str] = None,
):
    if number_of_sinks < 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    if number_of_commodes < 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    if number_of_bidets < 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    # select bathroom table to get how many bathrooms are in the household
    # to determine the bathroom number
    count = session.execute(
        """
        SELECT
            COUNT(*) AS count
        FROM (
            SELECT
                email,
                bathroom_number,
                number_of_bidets
            FROM half_bathroom
            UNION
            SELECT
                email,
                bathroom_number,
                number_of_bidets
            FROM full_bathroom
        ) AS subq
        NATURAL JOIN household
        WHERE email = :email
        """,
        {"email": email},
    ).fetchone()

    bathroom_number = count.count + 1
    session.execute(
        "INSERT INTO half_bathroom"
        " VALUES (:email, :bathroom_number, :number_of_sinks, :number_of_commodes, :number_of_bidets, :half_bath_name)",
        {
            "email": email,
            "bathroom_number": bathroom_number,
            "number_of_sinks": number_of_sinks,
            "number_of_commodes": number_of_commodes,
            "number_of_bidets": number_of_bidets,
            "half_bath_name": half_bath_name,
        },
    )

    session.commit()

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.post("/validate_primary_bathroom")
def validate_primary_bathroom(email: str):
    # only to be called upon bathroom form marked as primary bathroom
    # before calling the insert_full_bathroom function
    bath = session.execute(
        """
        SELECT
            email,
            bathroom_number
        FROM full_bathroom
        WHERE email = :email
        AND is_primary_bathroom = true
        """,
        {"email": email},
    ).fetchone()

    if bath:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Primary bathroom already exists",
                }
            ),
        )

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.post("/insert_full_bathroom")
def insert_full_bathroom(
    email: str,
    number_of_sinks: int,
    number_of_commodes: int,
    number_of_bidets: int,
    number_of_bathtubs: int,
    number_of_showers: int,
    number_of_tub_showers: int,
    is_primary_bathroom: bool,
):
    if number_of_sinks < 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    if number_of_commodes < 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    if number_of_bidets < 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    if number_of_bathtubs < 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    if number_of_showers < 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )
    if number_of_tub_showers < 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "success": False,
                    "message": "Invalid number",
                }
            ),
        )

    count = session.execute(
        """
        SELECT
            COUNT(*) AS count
        FROM (
            SELECT
                email,
                bathroom_number,
                number_of_bidets
            FROM half_bathroom
            UNION
            SELECT
                email,
                bathroom_number,
                number_of_bidets
            FROM full_bathroom
        ) AS subq
        NATURAL JOIN household
        WHERE email = :email
        """,
        {"email": email},
    ).fetchone()

    bathroom_number = count.count + 1

    # Query 8
    session.execute(
        "INSERT INTO full_bathroom"
        " VALUES (:email, :bathroom_number, :number_of_sinks, :number_of_commodes, :number_of_bidets, :number_of_bathtubs, :number_of_showers, :number_of_tub_showers,:is_primary_bathroom)",
        {
            "email": email,
            "bathroom_number": bathroom_number,
            "number_of_sinks": number_of_sinks,
            "number_of_commodes": number_of_commodes,
            "number_of_bidets": number_of_bidets,
            "number_of_bathtubs": number_of_bathtubs,
            "number_of_showers": number_of_showers,
            "number_of_tub_showers": number_of_tub_showers,
            "is_primary_bathroom": is_primary_bathroom,
        },
    )

    session.commit()

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.get("/get_current_bathrooms")
def get_current_bathrooms(email: str):
    bathrooms = session.execute(
        """
        SELECT
            email,
            bathroom_number,
            bathroom_type,
            is_primary_bathroom
        FROM (
            SELECT
                email,
                bathroom_number,
                'half' AS bathroom_type,
                false AS is_primary_bathroom
            FROM half_bathroom
            WHERE email = :email
            UNION
            SELECT
                email,
                bathroom_number,
                'full' AS bathroom_type,
                is_primary_bathroom AS is_primary_bathroom
            FROM full_bathroom
            WHERE email = :email
        ) AS bathroom_listing
        ORDER BY bathroom_number
        """,
        {"email": email},
    ).fetchall()

    return JSONResponse(content=jsonable_encoder(bathrooms))


@app.get("/get_all_manufacturers")
def get_all_manufacturers():
    manufacturers = session.execute(
        """
        SELECT
            id,
            manufacturer_name
        FROM manufacturer
        """
    ).fetchall()

    return JSONResponse(content=jsonable_encoder(manufacturers))


@app.post("/insert_appliance")
def insert_appliance(
    model: str,
    manufacturer_id: int,
    email: str,
    appliance_type: str,
):
    appliance_count = session.execute(
        """
        SELECT COUNT(*) as count
        FROM appliance
        WHERE email = :email
        """,
        {"email": email},
    ).fetchone()

    appliance_number = appliance_count.count + 1

    # Query 10
    session.execute(
        "INSERT INTO appliance"
        " VALUES (:appliance_number, :model, :manufacturer_id, :email, :appliance_type)",
        {
            "appliance_number": appliance_number,
            "model": model,
            "manufacturer_id": manufacturer_id,
            "email": email,
            "appliance_type": appliance_type,
        },
    )

    session.commit()

    return JSONResponse(
        content=jsonable_encoder(
            {
                "appliance_number": appliance_number,
            }
        )
    )


@app.post("/insert_dryer")
def insert_dryer(
    dryer_heat_source: str,
    appliance_number: int,
    email: str,
):
    # Qeury 11
    session.execute(
        "INSERT INTO dryer" " VALUES (:dryer_heat_source, :appliance_number, :email)",
        {
            "dryer_heat_source": dryer_heat_source,
            "appliance_number": appliance_number,
            "email": email,
        },
    )

    session.commit()

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.post("/insert_fridge")
def insert_fridge(
    fridge_type: str,
    appliance_number: int,
    email: str,
):
    # Qeury 12
    session.execute(
        "INSERT INTO fridge" " VALUES (:fridge_type, :appliance_number, :email)",
        {
            "fridge_type": fridge_type,
            "appliance_number": appliance_number,
            "email": email,
        },
    )

    session.commit()

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.post("/insert_washer")
def insert_washer(
    loading_type: str,
    appliance_number: int,
    email: str,
):
    # Qeury 13
    session.execute(
        "INSERT INTO washer" " VALUES (:loading_type, :appliance_number, :email)",
        {
            "loading_type": loading_type,
            "appliance_number": appliance_number,
            "email": email,
        },
    )

    session.commit()

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.post("/insert_tv")
def insert_tv(
    display_type: str,
    display_size: float,
    max_resolution: str,
    appliance_number: int,
    email: str,
):
    # Qeury 14
    session.execute(
        "INSERT INTO tv"
        " VALUES (:display_type, :display_size, :max_resolution, :appliance_number, :email)",
        {
            "display_type": display_type,
            "display_size": display_size,
            "max_resolution": max_resolution,
            "appliance_number": appliance_number,
            "email": email,
        },
    )

    session.commit()

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.post("/insert_cooktop")
def insert_cooktop(
    cooktop_heat_source: str,
    appliance_number: int,
    email: str,
):
    # Qeury 15
    session.execute(
        "INSERT INTO cooktop"
        " VALUES (:cooktop_heat_source, :appliance_number, :email)",
        {
            "cooktop_heat_source": cooktop_heat_source,
            "appliance_number": appliance_number,
            "email": email,
        },
    )

    session.commit()

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.post("/insert_oven")
def insert_oven(
    oven_type: str,
    appliance_number: int,
    email: str,
):
    # Qeury 16
    session.execute(
        "INSERT INTO oven" " VALUES (:oven_type, :appliance_number, :email)",
        {
            "oven_type": oven_type,
            "appliance_number": appliance_number,
            "email": email,
        },
    )

    session.commit()

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.post("/insert_oven_heat_source")
def insert_oven_heat_source(
    oven_heat_source: str,
    appliance_number: int,
    email: str,
):

    oven_heat_source_list = oven_heat_source.split(",")
    for heat_source in oven_heat_source_list:
        session.execute(
            "INSERT INTO oven_heat"
            " VALUES (NULL, :oven_heat_source, :appliance_number, :email)",
            {
                "oven_heat_source": heat_source,
                "appliance_number": appliance_number,
                "email": email,
            },
        )

    session.commit()

    return JSONResponse(content=jsonable_encoder({"success": True}))


@app.get("/get_current_appliances")
def get_current_appliances(email: str):
    # Query 18
    appliances = session.execute(
        """
        SELECT
            appliance_number,
            appliance_type,
            manufacturer_id,
            model
        FROM appliance
        WHERE email = :email
        ORDER BY appliance_number ASC
        """,
        {"email": email},
    ).fetchall()

    return JSONResponse(content=jsonable_encoder(appliances))


# ---------------------#
# Statistics Endpoints #


@app.get("/get_top_25_manufacturers")
def get_top_25_manufacturers():
    # Queruies 19 & 20

    manufacturers = session.execute(
        """
        SELECT
        manufacturer_name,
        COUNT(manufacturer_id) AS total_appliance_count
        FROM appliance
        INNER JOIN manufacturer ON appliance.manufacturer_id = manufacturer.id
        GROUP BY manufacturer_id
        ORDER BY COUNT(manufacturer_id) DESC
        LIMIT 25
        """
    ).fetchall()

    return JSONResponse(content=jsonable_encoder(manufacturers))


@app.get("/get_top_25_manufacturer_drilldown")
def get_top_25_manufacturer_drilldown(manufacturer_name: str):
    data = session.execute(
        """
    SELECT
    manufacturer_name,
    appliance_type,
    COUNT(appliance_type) AS total_appliance_count
    FROM appliance
    INNER JOIN manufacturer ON  appliance.manufacturer_id = manufacturer.id
    WHERE manufacturer_name = :manufacturer_name
    GROUP BY appliance.appliance_type
    """,
        {"manufacturer_name": manufacturer_name},
    ).fetchall()

    return JSONResponse(content=jsonable_encoder(data))


@app.get("/manufacturer_model_search")
def manufacturer_model_search(keyword: str):
    keyword = keyword.lower()
    # Query 21
    appliances = session.execute(
        """
        SELECT
            manufacturer_name AS Manufacturer,
            model AS Model
        FROM manufacturer
        INNER JOIN appliance ON appliance.manufacturer_id = manufacturer.id
        WHERE manufacturer_name LIKE :keyword
        OR model LIKE :keyword
        ORDER BY manufacturer_name ASC, model ASC
        """,
        {"keyword": f"%{keyword}%"},
    ).fetchall()

    return JSONResponse(content=jsonable_encoder(appliances))


@app.get("/avg_tv_size")
def avg_tv_size(state: Optional[str] = None):
    # Query 22 & 23
    if not state:
        avg_size = session.execute(
            """
            SELECT
                state,
                ROUND(AVG(display_size), 1) AS average_tv_size
            FROM tv
            INNER JOIN appliance ON tv.appliance_number = appliance.appliance_number
            AND tv.email = appliance.email
            INNER JOIN household ON appliance.email = household.email
            LEFT JOIN city_info ON household.postal_code = city_info.postal_code
            GROUP BY state
            ORDER BY state ASC
            """
        ).fetchall()
    else:
        avg_size = session.execute(
            """
            SELECT
                display_type,
                max_resolution,
                ROUND(AVG(display_size), 1) AS average_tv_size
            FROM tv
            INNER JOIN appliance ON tv.appliance_number = appliance.appliance_number
            AND tv.email = appliance.email
            INNER JOIN household ON appliance.email = household.email
            LEFT JOIN city_info ON household.postal_code = city_info.postal_code
            WHERE state = :state
            GROUP BY display_type, max_resolution
            ORDER BY display_type ASC, max_resolution ASC
            """,
            {"state": state},
        ).fetchall()

        if len(avg_size) == 0:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder(
                    {
                        "success": False,
                        "message": "No data has been found for the selected state.",
                    }
                ),
            )
    return JSONResponse(content=jsonable_encoder(avg_size))


@app.get("/extra_fridges")
def extra_fridges():
    # Query 24 & 25
    sum_of_fridges = session.execute(
        """
        SELECT COUNT(*) AS households_with_multiple_fridge_freezers FROM (
            SELECT
                household.email, COUNT(*) AS per_household_count
            FROM fridge
            INNER JOIN appliance ON fridge.appliance_number = appliance.appliance_number
            AND appliance.email = fridge.email
            INNER JOIN household ON appliance.email = household.email
            GROUP BY household.email
        ) AS subq
        WHERE per_household_count > 1
        """
    ).fetchone()

    subq = session.execute(
        """
        SELECT
            household.email
            FROM fridge
            INNER JOIN appliance
            ON
            fridge.appliance_number = appliance.appliance_number
            AND fridge.email = appliance.email
            INNER JOIN household ON appliance.email = household.email
            GROUP BY household.email
            HAVING COUNT(*) > 1
        """
    ).fetchall()

    emails = [email[0] for email in subq]

    fridges = session.execute(
        """
        SELECT
            state,
            ROUND(100*COUNT(CASE WHEN fridge_type = 'chest' THEN 1 ELSE NULL END) / COUNT(*)) AS chest_rate,
            ROUND(100*COUNT(CASE WHEN fridge_type = 'upright' THEN 1 ELSE NULL END) / COUNT(*)) AS upright_rate,
            ROUND(100*COUNT(CASE WHEN fridge_type != 'chest' AND fridge_type != 'upright' THEN 1 ELSE NULL END) / COUNT(*)) AS others_rate
        FROM
        city_info
        LEFT JOIN household ON city_info.postal_code = household.postal_code
        INNER JOIN appliance ON household.email = appliance.email
        INNER JOIN fridge
        ON
        appliance.appliance_number = fridge.appliance_number
        AND
        appliance.email = fridge.email
        WHERE appliance.email IN :emails
        GROUP BY state
        """,
        {
            "emails": emails,
        },
    ).fetchall()
    return JSONResponse(
        content=jsonable_encoder(
            {
                "sum_of_fridges": sum_of_fridges if sum_of_fridges else 0,
                "fridges": fridges,
            }
        )
    )


@app.get("/laundries")
def laundries():
    # Query 26 & 27

    loading_heat = session.execute(
        """
        SELECT
            subq_washer.state,
            loading_type,
            dryer_heat_source
        FROM (
            SELECT
                state,
                loading_type,
                COUNT(*) AS total_washer_households,
                ROW_NUMBER() OVER (PARTITION BY state ORDER BY COUNT(*) DESC) AS row_number_washer
            FROM washer
            INNER JOIN appliance ON washer.appliance_number = appliance.appliance_number
            AND washer.email = appliance.email
            INNER JOIN household ON appliance.email = household.email
            LEFT JOIN city_info ON household.postal_code = city_info.postal_code
            GROUP BY state, loading_type
        ) AS subq_washer
        LEFT JOIN (
            SELECT
                state,
                dryer_heat_source,
                COUNT(*) AS total_dryer_households,
                ROW_NUMBER() OVER (PARTITION BY state ORDER BY COUNT(*) DESC) AS row_number_dryer
            FROM dryer
            INNER JOIN appliance ON dryer.appliance_number = appliance.appliance_number
            AND dryer.email = appliance.email
            INNER JOIN household ON appliance.email = household.email
            LEFT JOIN city_info ON household.postal_code = city_info.postal_code
            GROUP BY state, dryer_heat_source
        ) AS subq_dryer
        ON subq_washer.state = subq_dryer.state
        WHERE row_number_washer = 1 AND row_number_dryer = 1
        """
    ).fetchall()

    washing_machine_no_dryer = session.execute(
        """
        SELECT DISTINCT(city_info.state) as state, COALESCE(count_washer, 0) FROM city_info
        LEFT JOIN (
            SELECT
                state,
                COUNT(*) AS count_washer
            FROM (
                SELECT
                    state,
                    subq_washer.email,
                    total_washer
                FROM (
                    SELECT
                        state,
                        email,
                        COUNT(*) AS total_washer
                    FROM washer
                    NATURAL JOIN appliance
                    NATURAL JOIN household
                    NATURAL JOIN city_info
                    GROUP BY state, email
                ) AS subq_washer
                INNER JOIN (
                    SELECT
                        email,
                        total_dryer
                    FROM (
                        SELECT
                            email,
                            COUNT(*) AS total_dryer
                        FROM dryer
                        NATURAL JOIN appliance
                        NATURAL JOIN household
                        GROUP BY email
                    ) AS subq_subq_dryer
                    WHERE total_dryer = 0
                ) subq_dryer
                ON subq_washer.email = subq_dryer.email
            ) AS main
            GROUP BY state
            ORDER BY COUNT(*) DESC
        ) AS subq
        ON city_info.state = subq.state
        """
    ).fetchall()

    return JSONResponse(
        content=jsonable_encoder(
            {
                "loading_heat": loading_heat,
                "washing_machine_no_dryer": washing_machine_no_dryer,
            }
        )
    )


@app.get("/bathrooms")
def bathrooms():
    # Query 28
    bathrooms_stats = session.execute(
        """
        SELECT
            MAX(count_baths) AS max_count_all_bathroom,
            MIN(count_baths) AS min_count_all_bathroom,
            AVG(count_baths) AS avg_count_all_bathroom
        FROM (
            SELECT
                email,
                COUNT(*) AS count_baths
            FROM (
                SELECT
                    email,
                    bathroom_number
                FROM half_bathroom
                UNION
                SELECT
                    email,
                    bathroom_number
                FROM full_bathroom
            ) AS subq
            NATURAL JOIN household
            GROUP BY email
        ) AS main
        """
    ).fetchall()

    # Query 29
    half_bathrooms = session.execute(
        """
        SELECT
            MAX(count_baths) AS max_count_half_bathroom,
            MIN(count_baths) AS min_count_half_bathroom,
            AVG(count_baths) AS avg_count_half_bathroom
        FROM (
            SELECT
                COUNT(*) as count_baths
            FROM half_bathroom
            NATURAL JOIN household
            GROUP BY email
        ) AS subq
        """
    ).fetchall()

    # Query 30
    full_bathrooms = session.execute(
        """
        SELECT
            MAX(count_baths) AS max_count_full_bathroom,
            MIN(count_baths) AS min_count_full_bathroom,
            AVG(count_baths) AS avg_count_full_bathroom
        FROM (
            SELECT
                COUNT(*) as count_baths
            FROM full_bathroom
            NATURAL JOIN household
            GROUP BY email
        ) AS subq
        """
    ).fetchall()

    # Query 31
    commodes = session.execute(
        """
        SELECT
            MAX(count_commodes) AS max_count_commodes,
            MIN(count_commodes) AS min_count_commodes,
            AVG(count_commodes) AS avg_count_commodes
        FROM (
            SELECT
                SUM(number_of_commodes) AS count_commodes
            FROM (
                SELECT
                    email,
                    bathroom_number,
                    number_of_commodes
                FROM half_bathroom
                UNION
                SELECT
                    email,
                    bathroom_number,
                    number_of_commodes
                FROM full_bathroom
            ) AS subq
        NATURAL JOIN household
        GROUP BY email
        ) AS main
        """
    ).fetchall()

    # Query 32
    sinks = session.execute(
        """
        SELECT
            MAX(count_sinks) AS max_count_sinks,
            MIN(count_sinks) AS min_count_sinks,
            AVG(count_sinks) AS avg_count_sinks
        FROM (
            SELECT
                SUM(number_of_sinks) AS count_sinks
            FROM (
                SELECT
                    email,
                    bathroom_number,
                    number_of_sinks
                FROM half_bathroom
                UNION
                SELECT
                    email,
                    bathroom_number,
                    number_of_sinks
                FROM full_bathroom
            ) AS subq
        NATURAL JOIN household
        GROUP BY email
        ) AS main
        """
    ).fetchall()

    # Query 33
    bidets = session.execute(
        """
        SELECT
            MAX(count_bidets) AS max_count_bidets,
            MIN(count_bidets) AS min_count_bidets,
            AVG(count_bidets) AS avg_count_bidets
        FROM (
            SELECT
                SUM(number_of_bidets) AS count_bidets
            FROM (
                SELECT
                    email,
                    bathroom_number,
                    number_of_bidets
                FROM half_bathroom
                UNION
                SELECT
                    email,
                    bathroom_number,
                    number_of_bidets
                FROM full_bathroom
            ) AS subq
            NATURAL JOIN household
            GROUP BY email
        ) AS main
        """
    ).fetchall()

    # Query 34
    bathtubs = session.execute(
        """
        SELECT
            MAX(count_bathtubs) AS max_count_bathtubs,
            MIN(count_bathtubs) AS min_count_bathtubs,
            AVG(count_bathtubs) AS avg_count_bathtubs
        FROM (
            SELECT
                SUM(number_of_bathtubs) AS count_bathtubs
            FROM full_bathroom
            NATURAL JOIN household
            GROUP BY email
        ) AS subq
        """
    ).fetchall()

    # Query 35
    showers = session.execute(
        """
        SELECT
            MAX(count_showers) AS max_count_showers,
            MIN(count_showers) AS min_count_showers,
            AVG(count_showers) AS avg_count_showers
        FROM (
            SELECT
                SUM(number_of_showers) AS count_showers
            FROM full_bathroom
            NATURAL JOIN household
            GROUP BY email
        ) AS subq
        """
    ).fetchall()

    # Query 36
    tub_showers = session.execute(
        """
        SELECT
            MAX(count_tub_showers) AS max_count_tub_showers,
            MIN(count_tub_showers) AS min_count_tub_showers,
            AVG(count_tub_showers) AS avg_count_tub_showers
        FROM (
            SELECT
                COUNT(number_of_tub_showers) AS count_tub_showers
            FROM full_bathroom
            NATURAL JOIN household
            GROUP BY email
        ) AS subq
        """
    ).fetchall()

    # Query 37
    state_most_bidets = session.execute(
        """
        SELECT
            state,
            SUM(number_of_bidets) AS total_bidets
        FROM (
            SELECT
                email,
                bathroom_number,
                number_of_bidets
            FROM half_bathroom
            UNION
            SELECT
                email,
                bathroom_number,
                number_of_bidets
            FROM full_bathroom
        ) AS subq
        NATURAL JOIN household
        NATURAL JOIN city_info
        GROUP BY state
        ORDER BY total_bidets DESC
        LIMIT 1
        """
    ).fetchone()

    # Query 38
    postal_code_most_bidets = session.execute(
        """
        SELECT
            postal_code,
            SUM(number_of_bidets) AS total_bidets
        FROM (
            SELECT
                email,
                bathroom_number,
                number_of_bidets
            FROM half_bathroom
            UNION
            SELECT
                email,
                bathroom_number,
                number_of_bidets
            FROM full_bathroom
        ) AS subq
        NATURAL JOIN household
        NATURAL JOIN city_info
        GROUP BY postal_code
        ORDER BY total_bidets DESC
        LIMIT 1
        """
    ).fetchone()

    # Query 39
    household_one_primary_bathroom = session.execute(
        """
        SELECT
            COUNT(email) AS only_single_primary
        FROM (
            SELECT
                email,
                is_primary_bathroom,
                COUNT(*) AS count_baths
            FROM (
                SELECT
                    email,
                    bathroom_number,
                    false AS is_primary_bathroom
                FROM half_bathroom
                UNION
                SELECT
                    email,
                    bathroom_number,
                    is_primary_bathroom
                FROM full_bathroom
            ) AS subq
            GROUP BY email, is_primary_bathroom
        ) AS main
        NATURAL JOIN household
        WHERE count_baths = 1
        AND is_primary_bathroom = true
        """
    ).fetchone()

    print(bathrooms_stats)

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(
            {
                "bathrooms": bathrooms_stats,
                "half_bathrooms": half_bathrooms,
                "full_bathrooms": full_bathrooms,
                "commodes": commodes,
                "sinks": sinks,
                "bidets": bidets,
                "bathtubs": bathtubs,
                "showers": showers,
                "tub_showers": tub_showers,
                "state_most_bidets": state_most_bidets,
                "postal_code_most_bidets": postal_code_most_bidets,
                "household_one_primary_bathroom": household_one_primary_bathroom,
            },
        ),
    )


@app.get("/household_radius")
async def household_radius(postal_code: int, radius: Union[int, float]):

    # Query 40
    city = session.execute(
        """
        SELECT
            postal_code,
            longitude,
            latitude
        FROM city_info
        WHERE postal_code = :postal_code
        """,
        {
            "postal_code": postal_code,
        },
    ).one_or_none()

    if city is None:
        return JSONResponse(
            {
                "status_code": 404,
                "error": "Postal code not found",
            }
        )
    # account for rounding errors
    radius += 0.01

    # Haversine formula
    session.execute(
        """
    DROP FUNCTION IF EXISTS haversine;
    CREATE FUNCTION haversine (lat1 FLOAT, lon1 FLOAT, lat2 FLOAT, lon2 FLOAT)
    RETURNS FLOAT DETERMINISTIC
    BEGIN
        DECLARE r_lon FLOAT;
        DECLARE r_lat FLOAT;
        DECLARE a FLOAT;
        DECLARE c FLOAT;
        DECLARE d FLOAT;

        SET r_lon = RADIANS(lon2 - lon1);
        SET r_lat = RADIANS(lat2 - lat1);
        SET a = SIN(r_lat / 2) * SIN(r_lat / 2) + COS(RADIANS(lat1)) * COS(RADIANS(lat2)) * SIN(r_lon / 2) * SIN(r_lon / 2);
        SET c = 2 * ATAN2(SQRT(a), SQRT(1 - a));
        SET d = 3958.75 * c;

        RETURN d;
    END;
    """
    )

    filtered_cities = session.execute(
        """
        SELECT postal_code, longitude, latitude
        FROM city_info
        WHERE haversine(latitude, longitude, :center_latitude, :center_longitude) <= :radius
        """,
        {
            "center_latitude": city.latitude,
            "center_longitude": city.longitude,
            "radius": radius,
        },
    ).fetchall()

    # Query 41
    bathroom_count = session.execute(
        """
        SELECT AVG(bathroom_count)
        FROM (
            SELECT
                COUNT(*) as bathroom_count
            FROM household
            NATURAL JOIN city_info
            LEFT JOIN (
                SELECT
                    email,
                    bathroom_number
                FROM (
                    SELECT
                        email,
                        bathroom_number
                    FROM half_bathroom
                    UNION
                    SELECT
                        email,
                        bathroom_number
                    FROM full_bathroom
                ) AS subq
            ) AS subq_bathroom ON household.email = subq_bathroom.email
            WHERE haversine(latitude, longitude, :center_latitude, :center_longitude) <= :radius
            GROUP BY household.email
        ) AS bathroom_per_households
        """,
        {
            "center_longitude": city.longitude,
            "center_latitude": city.latitude,
            "radius": radius,
        },
    ).fetchone()

    # Query 42
    bedrooms_count = session.execute(
        """
        SELECT
            AVG(number_of_bedrooms)
        FROM household
        NATURAL JOIN city_info
        WHERE haversine(latitude, longitude, :center_latitude, :center_longitude) <= :radius
        """,
        {
            "center_longitude": city.longitude,
            "center_latitude": city.latitude,
            "radius": radius,
        },
    ).fetchone()

    # Query 43
    occupants_count = session.execute(
        """
        SELECT
            AVG(number_of_occupants)
        FROM household
        NATURAL JOIN city_info
        WHERE haversine(latitude, longitude, :center_latitude, :center_longitude) <= :radius
        """,
        {
            "center_longitude": city.longitude,
            "center_latitude": city.latitude,
            "radius": radius,
        },
    ).fetchone()

    # Query 44
    occupants_vs_commodes = session.execute(
        """
        SELECT
            AVG(ratio_commodes_occupants)
        FROM (
            SELECT
                household.email,
                number_of_occupants / SUM(number_of_commodes) as ratio_commodes_occupants
            FROM household
            NATURAL JOIN city_info
            LEFT JOIN (
                SELECT
                    email,
                    bathroom_number,
                    number_of_commodes
                FROM (
                    SELECT
                        email,
                        bathroom_number,
                        number_of_commodes
                    FROM half_bathroom
                    UNION
                    SELECT
                        email,
                        bathroom_number,
                        number_of_commodes
                    FROM full_bathroom
                ) AS subq
            ) AS subq_bathroom ON household.email = subq_bathroom.email
            WHERE haversine(latitude, longitude, :center_latitude, :center_longitude) <= :radius
            GROUP BY household.email, number_of_occupants
        ) AS ratio_commodes_occupants
        """,
        {
            "center_longitude": city.longitude,
            "center_latitude": city.latitude,
            "radius": radius,
        },
    ).fetchone()

    # Query 45
    appliances_count = session.execute(
        """
        SELECT
            AVG(appliances_per_households)
        FROM (
            SELECT
                COUNT(*) as appliances_per_households
            FROM household
            NATURAL JOIN city_info
            LEFT JOIN appliance
            ON household.email = appliance.email
            WHERE haversine(latitude, longitude, :center_latitude, :center_longitude) <= :radius
            GROUP BY household.email
        ) AS appliances_per_households
        """,
        {
            "center_longitude": city.longitude,
            "center_latitude": city.latitude,
            "radius": radius,
        },
    ).fetchone()

    # Query 46
    common_heatsource = session.execute(
        """
        SELECT
            heat_source
        FROM (
            SELECT
                email,
                appliance_number,
                dryer_heat_source AS heat_source
            FROM dryer
            UNION
            SELECT
                email,
                appliance_number,
                cooktop_heat_source AS heat_source
            FROM cooktop
            UNION
            SELECT
                oven.email,
                oven.appliance_number,
                oven_heat_source AS heat_source
            FROM oven
            LEFT JOIN oven_heat
            ON oven.email = oven_heat.email AND oven.appliance_number = oven_heat.appliance_number
        ) AS heat_sources
        NATURAL JOIN household
        NATURAL JOIN city_info
        WHERE haversine(latitude, longitude, :center_latitude, :center_longitude) <= :radius
        GROUP BY heat_source
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """,
        {
            "center_longitude": city.longitude,
            "center_latitude": city.latitude,
            "radius": radius,
        },
    ).fetchone()

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(
            {
                "filtered_postal_codes": filtered_cities,
                "bathroom_count": bathroom_count,
                "bedrooms_count": bedrooms_count,
                "occupants_count": occupants_count,
                "occupants_vs_commodes": occupants_vs_commodes,
                "appliances_count": appliances_count,
                "common_heatsource": common_heatsource,
            },
        ),
    )
