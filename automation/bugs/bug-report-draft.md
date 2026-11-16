# Bug report candidates from HW04 UI execution

These are local reproduction candidates found by Playwright against the EShop UI with controlled API responses. Confirm each against the live backend before filing a public GitHub Issue. Add a fresh screenshot/trace and environment details from the final matrix run.

| ID | Requirement | Observation | Reproduction |
|---|---|---|---|
| BUG-FR04-01 | FR-04 phone must begin with `0` and have 10–11 digits | The profile form uses a pattern that rejects valid numbers beginning with `0` and accepts some numbers beginning with `1` that violate the requirement. | Open Profile, enter name/address and phone `0912345678`, save; observe validation rejects it. Then try `1234567890`; observe the UI submits it. |
| BUG-FR15-01 | FR-15 product name max 255 chars | Product form has no max length guard; 256-character name is submitted to the API. | Admin → Products; enter 256 chars and a positive price, save; observe POST. |
| BUG-FR15-02 | FR-15 product price must be positive | Product form has no positive minimum validation; zero and negative prices can be submitted. | Admin → Products; enter a name and price `0` (then `-1`), save; observe POST. |
| BUG-FR15-03 | FR-15 editing one product must not change other products | Client state update maps every product to the edited name after a successful edit. | In a controlled two-product list, edit Existing Alpha; observe Existing Beta disappear/change in the table. |
| BUG-FR15-04 | FR-15 category is required | Product form has no required guard on category; when the category list is empty, submit remains possible. | Load the Admin product form with an empty category response, enter name and positive price, and save; inspect the outgoing POST. |

Do not publish these as confirmed GitHub Issues until the live SUT/backend behavior is reproduced and the screenshot is captured from that reproduction.
