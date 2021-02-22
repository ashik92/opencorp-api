## Sample command

```bash
    python3 script.py -country au -pages 100 -created_at 2021-02-22
```
- `-created_at` - here created date is used as **before date(:created_at)** documentarion is here- https://api.opencorporates.com/documentation/API-Reference#date-filter 
- the number of `-pages` the number of `API` call
- `-country` - country code must be included in the config file



## Some Useful Links

**OpenCorporates - API Doc**
https://api.opencorporates.com/documentation/API-Reference

**OpenCorporates - all available companies**
https://opencorporates.com/registers

**OpenCorporates - Account Status:** 
https://api.opencorporates.com/v0.4/account_status?api_token=z9l30RgC5L7GCpiZZ9ix

**Example URL (i.e malaysia data ):**
https://api.opencorporates.com/companies/search?api_token=z9l30RgC5L7GCpiZZ9ix&country_code=my&fields=normalised_name&inactive=false&per_page=100&order=created_at