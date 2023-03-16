# CS6400 -- Phase 2 Abstract Code + SQL (Team 101)

## Email Form

### Abstract Code

- User enters email (‘$Email’) in input field
-   When Submit button is pressed: 
        - Run "SELECT" query on database to get all rows from the main household table where email = `$Email` (1)
        - If Email is already in database (i.e. if query > 0):
            - Go back to Email Form with error message
        - Else (if query = 0): 
            - Proceed to Postal Code Search

### Queries

#### (1) Select on Email table

```SQL
    SELECT COUNT(email)
    FROM household
    WHERE email = '$Email'
```

## Postal Code Search

### Abstract Code

- User enters postal code (‘$Postal_Code’) in input field
    - When Submit button is pressed: 
        - Run "SELECT" query on database to get row from the city_info table where postal code = `$Postal_Code` (2)
        - If postal code is in database of postal codes (i.e. if query returns 1 row):
            - Display Query Result (2)
            - Ask User if the information is correct
            - When Yes button is selected: 
                - Proceed to Phone Number Form
            - When No button is selected: 
                - Return to beginning of Postal Code Form
        - Else (i.e. if query returns 0 rows):
            - return Postal Code Form with error message

### Queries

#### (2) Select on Postal Code table

```SQL
    SELECT postal_code, city, state
    FROM city_info
    WHERE postal_code = '$Postal_Code'
```

## Phone Number Form

### Abstract Code

- Ask user if they would like to enter a phone number
- If Yes button is selected:
    - Display Area Code, Number, and Phone type text entries fields
    - User enters area code (‘$Area_Code’) in input field
    - User enters remaining 7 digits (‘$7_Digits’) in input field
    - User Selects phone type (‘$Phone_Type’) from drop down list of: home, mobile, work or other
    - Run a "SELECT" statement on the phone_info table to check if the phone number is already in the database (3)

    - If there is a match (i.e. if query > 0):
        - Show error message
    - Else (i.e. if query = 0):
        - Run an "INSERT" statement on the phone_info table to add the phone number to the database (4)
        - When Next button is selected:
            - Proceed to Household Info Form
- If No button is selected: 
    - Proceed to Household Info Form

### Queries

#### (3) Select on Phone Info table

```SQL
    SELECT COUNT(phone_number)
    FROM phone_info
    WHERE area_code = '$Area_Code'
    AND 7_digits = '$7_Digits'
```

#### (4) Insert into Phone Info table

```SQL
    INSERT INTO phone_info 
    (area_code, 7_digits, phone_type, email)
    VALUES ('$Area_Code', '$7_Digits', '$Phone_Type', '$Email'*)
```

## Household Info Form

### Abstract Code

- User selects home type (‘$Home_Type’) from a drop down list of: house, apartment, townhome, condominium, or mobile home
- User enters square footage (‘$Square_Footage’) in input field
- User enters number of occupants (‘$Number_Of_Occupants’) in input field
- User enters number of bedrooms (‘$Number_Of_Bedrooms’) in input field
- When Next button is selected: 
    - Run an "INSERT" statement on the household table to add the household information to the database (5)
    - Proceed to Bathroom Info Form

### Queries

#### (5) Insert into Household table

```SQL
    INSERT INTO household 
    (email, home_type, square_footage, number_of_occupants, number_of_bedrooms, postal_code
    VALUES (
        '$Email', 
        '$Home_Type', 
        '$Square_Footage', 
        '$Number_Of_Occupants', 
        '$Number_Of_Bedrooms', 
        '$Postal_Code'*
    )
```

## Bathroom Info Form

### Abstract Code

- Initialize ‘$Bathroom_#’ = 0
- Ask user if they have a half bathroom 
- If Yes is selected (tab selecting “half”): 
    - User enters sinks (‘$Number_of_Sinks’) in input field
    - User enters commodes (‘$Number_of_Commodes’) in input field
    - User enters bidets (‘$Number_of_Bidets’) in input field
    - User enters half bath name (‘$Half_Bath_Name’) in input field (This field is optional)
    - When Add is selected: 
        - Increment bathroom # (‘$Bathroom_#’) by 1
        - Run an "INSERT" statement on the half bathroom table to add the bathroom information to the database (6)
        - Jump to bathroom listing
- If No is selected (tab selecting “full”): 
    - User enters sinks (‘$Number_of_Sinks’) in input field
    - User enters commodes (‘$Number_of_Commodes’) in input field
    - User enters bidets (‘$Number_of_Bidets’) in input field
    - User enters bathtubs (‘$Number_of_Bathtubs’) in input field
    - User enters showers (‘$Number_of_Showers’) in input field
    - User enters tub/shower (‘$Number_of_TubShowers’) in input field

    - Run "SELECT" statement on the full bathroom table to check if any of the already entered bathroom is marked as primary (7)
    - If primary bathroom variable (‘$Is_Primary_Bathroom’) is not yet entered (i.e. if query = false):
        - User may select the "is primary bathroom" (‘$Is_Primary_Bathroom’) check box
    - Else: (i.e. query = true) 
        - User can not select check box
    - When Add is selected: 
        - Increment bathroom # (‘$Bathroom_#’) by 1
        - Run an "INSERT" statement on the full bathroom table to add the bathroom information to the database (8)
        - Jump to bathroom listing

- If No is selected (Cannot happen if user interface is used correctly): 
    - Display an error message indicating that the user must have one bathroom 
    - Return to Bathroom Info Form


### Queries

#### (6) Insert into Half Bathroom table

```SQL
    INSERT INTO half_bathroom 
    (email, bathroom_number, number_of_sinks, number_of_commodes, number_of_bidets, half_bath_name)
    VALUES (
        '$Email', 
        '$Bathroom_#', 
        '$Number_of_Sinks', 
        '$Number_of_Commodes', 
        '$Number_of_Bidets', 
        '$Half_Bath_Name'
    )
```

#### (7) Select from Full Bathroom table

```SQL
    SELECT EXISTS(is_primary_bathroom)
    FROM full_bathroom
    WHERE email = '$Email'
    AND is_primary_bathroom = true
```

#### (8) Insert into Full Bathroom table

```SQL
    INSERT INTO full_bathroom 
    (email, bathroom_number, number_of_sinks, number_of_commodes, number_of_bidets, number_of_bathtubs, number_of_showers, number_of_tubshowers, is_primary_bathroom)
    VALUES (
        '$Email', 
        '$Bathroom_#', 
        '$Number_of_Sinks', 
        '$Number_of_Commodes', 
        '$Number_of_Bidets', 
        '$Number_of_Bathtubs', 
        '$Number_of_Showers', 
        '$Number_of_TubShowers', 
        '$Is_Primary_Bathroom'
    )
```

## Bathroom Listing

### Abstract Code

- Run "SELECT" statement on the both bathroom tables to get all bathrooms associated with the email (9) (Since this will be shown after each entry of households, there must exist at least one data to display.)
- User responds if they want to Add another bathroom
- When Add Another Bathroom is selected:
    - Return to the beginning of Bathroom Form
- When Next is selected: 
    - Continue to Appliance Form

### Queries

#### (9) Select from Full Bathroom table

```SQL
SELECT bathroom_number, bathroom_type, is_primary_bathroom FROM (
    SELECT bathroom_number, 'half' AS bathroom_type, false AS is_primary_bathroom
    FROM half_bathroom
    WHERE email = '$Email'
    UNION
    SELECT bathroom_number, 'full' AS bathroom_type, is_primary_bathroom AS is_primary_bathroom
    FROM full_bathroom
    WHERE email = '$Email'
) AS bathroom_listing
ORDER BY bathroom_number
```

## Appliances Info Form

### Abstract Code

- Initialize ‘$Appliance_#’ = 0
- User selects appliance type (‘$Appliance_Type) from a drop down list of: dryer, fridge, TV, washer, and - cooker.
- User selects manufacturer (‘$Manufacturer’) from a drop down list of manufacturers. 
- User enters model (‘$Model') in input field (This field is optional)

- If appliance type Dryer is selected:
    - set ‘$Appliance_Type’ = dryer
    - set $Dryer = true
    - User selects heat source (‘$Heat_Source) from a drop down list of: gas, electric, or none

- If appliance type Fridge is selected:
    - set ‘$Appliance_Type’ = fridge
    - set $Fridge = true
    - User selects fridge type (‘$Fridge_Type) from a drop down list of: bottom freezer refrigerator, French door refrigerator, side-by-side refrigerator, top freezer refrigerator, chest freezer, or upright freezer.

- If appliance type Washer is selected:
    - set ‘$Appliance_Type’ = washer
    - set $Washer = true
    - User selects loading type (‘$Loading_Type) from a drop down list of: top or front

- If appliance type TV is selected:
    - set ‘$Appliance_Type’ = TV
    - set $TV = true
    - User selects display type (‘$Display_Type) from a drop down list of: tube, DLP, plasma, LCD, or LED
    - User selects max resolution (‘$Max_Resolution) from a drop down list of: 480i, 576i, 720p, 1080i, 1080p, - 1440p, 2160p (4K), or 4320p (8K)
    - User enters display size(‘$Display_Size) in input field

- If appliance type Cooker is selected:
    - set ‘$Appliance_Type’ = cooker
    - User selects Oven or Cooktop checkbox
    - If Cooktop is checked: 
        - set $Cooktop = true
        - User selects cook heat source (‘$Cook_Heat_Source’) from a drop down list of: gas, electric, radiant electric, or induction
    - If Oven is checked: 
        - set $Oven = true
        - User selects oven heat source (‘$Oven_Heat_Source’) from a checkbox list of: gas, electric, and or microwave
        - User selects oven type (‘$Oven_Type’) from a drop down list of: gas, electric, radiant electric, or induction
- When Add button is selected:
    - Increment appliance # (‘$Appliance_#’) by 1
    - Run an "INSERT" statement on the appliance table to add the appliance information to the database (10)

    - if $Dryer = true:
        - Run an "INSERT" statement on the dryer table to add the dryer information to the database (11)
    - if $Fridge = true:
        - Run an "INSERT" statement on the fridge table to add the fridge information to the database (12)
    - if $Washer = true:
        - Run an "INSERT" statement on the washer table to add the washer information to the database (13)
    - if $TV = true:
        - Run an "INSERT" statement on the TV table to add the TV information to the database (14)
    - if $Cooktop = true:
        - Run an "INSERT" statement on the cooktop table to add the cooktop information to the database (15)
    - if $Oven = true:
        - Run an "INSERT" statement on the oven table to add the oven information to the database (16)
        - For each oven heat source selected:
            - Run an "INSERT" statement on the oven_heat_source table to add the oven heat source information to the database (17)
    
    - Jump to appliance listing

### Queries

#### (10) Insert into Appliance table

```SQL
    INSERT INTO appliance 
    (email, appliance_number, appliance_type, manufacturer, model, type)
    VALUES (
        '$Email', 
        '$Appliance_#', 
        '$Appliance_Type', 
        '$Manufacturer', 
        '$Model',
        '$Appliance_Type'
    )
```

#### (11) Insert into Dryer table

```SQL
    INSERT INTO dryer 
    (email, appliance_number, heat_source)
    VALUES (
        '$Email', 
        '$Appliance_#', 
        '$Heat_Source'
    )
```

#### (12) Insert into Fridge table

```SQL
    INSERT INTO fridge 
    (email, appliance_number, fridge_type)
    VALUES (
        '$Email', 
        '$Appliance_#', 
        '$Fridge_Type'
    )
```

#### (13) Insert into Washer table

```SQL
    INSERT INTO washer 
    (email, appliance_number, loading_type)
    VALUES (
        '$Email', 
        '$Appliance_#', 
        '$Loading_Type'
    )
```

#### (14) Insert into TV table

```SQL
    INSERT INTO TV 
    (email, appliance_number, display_type, max_resolution, display_size)
    VALUES (
        '$Email', 
        '$Appliance_#', 
        '$Display_Type', 
        '$Max_Resolution', 
        '$Display_Size'
    )
```

#### (15) Insert into Cooktop table

```SQL
    INSERT INTO cooktop 
    (email, appliance_number, cook_heat_source)
    VALUES (
        '$Email', 
        '$Appliance_#', 
        '$Cook_Heat_Source'
    )
```

#### (16) Insert into Oven table

```SQL
    INSERT INTO oven 
    (email, appliance_number, oven_heat_source, oven_type)
    VALUES (
        '$Email', 
        '$Appliance_#', 
        '$Oven_Type'
    )
```

#### (17) Insert into Oven_Heat_Source table

```SQL
    INSERT INTO oven_heat_source 
    (email, appliance_number, oven_heat_source)
    VALUES (
        '$Email', 
        '$Appliance_#', 
        '$Oven_Heat_Source'
    )
```

## Appliance Listing

### Abstract Code
- Run a "SELECT" statement on the appliance table to get the appliance information from the database (18)
- Display a table of all appliances types added in the order in which they were added (appliance ID) as well the manufacturer and model
- User responds if they want to Add another appliance
- When Add Another Appliance is selected:
    - Return to the beginning of Appliance Form
- When Next is selected: 
    - Continue to Done Screen

### Queries

#### (18) Select from Appliance table

```SQL
    SELECT email, appliance_number, appliance_type, manufacturer, model, type FROM appliance
    WHERE email = '$Email'
    ORDER BY appliance_number ASC
```