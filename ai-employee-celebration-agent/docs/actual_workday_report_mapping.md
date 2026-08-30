# Actual Workday Report Mapping

This project supports the exact RaaS JSON output from `RPT_AI_Employee_Celebration_Agent`.

## Report JSON Shape

The app expects Workday RaaS JSON in this shape:

```json
{
  "Report_Entry": [
    {
      "Active": "Active",
      "CF-LRV-Manager_Email_Id": "manager@example.com",
      "Country_of_position_location_on_worker_profile": "United States of America",
      "Date_of_Workers_Next_Birthday": "2027-05-25",
      "Email_-_Primary_Work_or_Primary_Home": "user@example.com",
      "Employee_ID": "21001",
      "Legal_Name_-_First_Name": "Logan",
      "Legal_Name_-_Last_Name": "McNeil",
      "Original_Hire_Date": "2000-01-01",
      "Preferred_Name": "Logan McNeil",
      "Supervisory_Organization": "Human Resources",
      "Time_Zone_of_Location_of_Worker_s_Primary_Position": "GMT-08:00 Pacific Time (Los Angeles)"
    }
  ]
}
```

## Field Mapping

| App Field | Workday Report Field |
|---|---|
| employee_id | Employee_ID |
| preferred_name | Preferred_Name |
| legal_first_name | Legal_Name_-_First_Name |
| legal_last_name | Legal_Name_-_Last_Name |
| email | Email_-_Primary_Work_or_Primary_Home |
| manager_email | CF-LRV-Manager_Email_Id |
| status | Active |
| country | Country_of_position_location_on_worker_profile |
| next_birthday_date | Date_of_Workers_Next_Birthday |
| original_hire_date | Original_Hire_Date |
| department | Supervisory_Organization |
| timezone | Time_Zone_of_Location_of_Worker_s_Primary_Position |

## Event Logic

Birthday detection uses an exact date match:

```text
Date_of_Workers_Next_Birthday == run date
```

Work anniversary detection uses the month/day from `Original_Hire_Date` and calculates completed years.

```text
Original_Hire_Date month/day == run date month/day
```

## Time Zone Handling

The report may return Workday labels such as:

```text
GMT-08:00 Pacific Time (Los Angeles)
```

The app normalizes this to:

```text
America/Los_Angeles
```

Other common values such as Eastern, Central, Mountain, India, London, UTC, and GMT are also normalized.

## Security Notes

- The actual RaaS URL should be stored only in local `.env`.
- Do not commit `.env`, ISU password, bearer token, or real employee output files.
- Using `Date_of_Workers_Next_Birthday` is better than exposing full date of birth because it reduces sensitive personal data exposure.
