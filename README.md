# ClearPath Health — Insurance Discharge System
A college demo prototype connecting hospitals and insurance providers for real-time bill verification and discharge coordination.

## Quick Start
```bash
pip install flask
python app.py
# Open http://localhost:5000
```

## Demo Credentials
| Role | Username | Password |
|------|----------|----------|
| Hospital Staff | `staff1` | `pass123` |
| Hospital Staff | `staff2` | `pass123` |
| Insurance Officer | `ins1` | `pass123` |
| Insurance Officer | `ins2` | `pass123` |

## Workflow
1. **Login** as Hospital Staff → `/hospital`
2. **Admit Patient** using the "+ Admit Patient" button
3. **Add Treatments** at `/treatment` — select patient, add procedures/costs
4. **Generate Bill** at `/bill` — review and click "Send to Insurance"
5. **Login** as Insurance Officer → `/insurance`
6. **Review & Approve** the claim
7. **Login** as Hospital Staff → `/discharge`
8. **Discharge Patient** — button unlocks after approval

## Structure
```
healthcare_discharge/
├── app.py                  # Flask backend (mock DB)
├── requirements.txt
├── static/css/style.css    # Shared stylesheet
└── templates/
    ├── login.html
    ├── hospital.html        # Hospital dashboard
    ├── treatment.html       # Treatment entry
    ├── bill.html            # Bill summary + submit
    ├── insurance.html       # Insurance claims dashboard
    ├── discharge.html       # Discharge page
    └── _hospital_sidebar.html
```
