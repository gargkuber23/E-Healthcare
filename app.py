from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'healthcare_demo_secret_2024'

# ── Mock Database ──────────────────────────────────────────────────────────────
USERS = {
    'staff1':    {'password': 'pass123', 'role': 'hospital', 'name': 'Dr. Sarah Mitchell'},
    'staff2':    {'password': 'pass123', 'role': 'hospital', 'name': 'Nurse James Carter'},
    'ins1':      {'password': 'pass123', 'role': 'insurance', 'name': 'Alex Reynolds'},
    'ins2':      {'password': 'pass123', 'role': 'insurance', 'name': 'Maria Santos'},
}

patients = {
    'P001': {
        'id': 'P001', 'name': 'Robert Chen', 'age': 54,
        'insurance_id': 'INS-8821', 'diagnosis': 'Acute Appendicitis',
        'admitted': '2024-01-15', 'status': 'admitted', 'ward': 'Surgical Wing B'
    },
    'P002': {
        'id': 'P002', 'name': 'Emily Hartman', 'age': 38,
        'insurance_id': 'INS-4432', 'diagnosis': 'Pneumonia',
        'admitted': '2024-01-17', 'status': 'admitted', 'ward': 'General Ward 3'
    },
    'P003': {
        'id': 'P003', 'name': 'James Okafor', 'age': 67,
        'insurance_id': 'INS-7791', 'diagnosis': 'Hip Fracture',
        'admitted': '2024-01-12', 'status': 'discharged', 'ward': 'Orthopedic Unit'
    },
}

treatments = {
    'P001': [
        {'id': 'T001', 'procedure': 'Appendectomy Surgery', 'cost': 18500, 'date': '2024-01-16', 'doctor': 'Dr. K. Patel'},
        {'id': 'T002', 'procedure': 'Anesthesia',           'cost': 3200,  'date': '2024-01-16', 'doctor': 'Dr. L. Torres'},
        {'id': 'T003', 'procedure': 'ICU Recovery (2 days)', 'cost': 5800, 'date': '2024-01-17', 'doctor': 'Dr. K. Patel'},
        {'id': 'T004', 'procedure': 'Medication & Antibiotics', 'cost': 1240, 'date': '2024-01-17', 'doctor': 'Pharmacy'},
    ],
    'P002': [
        {'id': 'T005', 'procedure': 'Chest X-Ray',           'cost': 850,  'date': '2024-01-17', 'doctor': 'Dr. M. Singh'},
        {'id': 'T006', 'procedure': 'IV Antibiotics (3 days)', 'cost': 2100, 'date': '2024-01-18', 'doctor': 'Dr. M. Singh'},
        {'id': 'T007', 'procedure': 'Pulmonary Function Test', 'cost': 1200, 'date': '2024-01-19', 'doctor': 'Dr. R. Nair'},
    ],
    'P003': [],
}

bills = {
    'B001': {
        'id': 'B001', 'patient_id': 'P001',
        'total': 28740, 'status': 'pending',
        'submitted_at': '2024-01-18 09:30',
        'notes': '', 'reviewed_by': None, 'reviewed_at': None
    },
    'B002': {
        'id': 'B002', 'patient_id': 'P002',
        'total': 4150, 'status': 'approved',
        'submitted_at': '2024-01-19 11:00',
        'notes': 'All procedures verified and within policy limits.',
        'reviewed_by': 'Alex Reynolds', 'reviewed_at': '2024-01-19 14:22'
    },
}

patient_counter = [4]
bill_counter    = [3]
treatment_counter = [8]

# ── Auth ───────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        user = USERS.get(username)
        if user and user['password'] == password:
            session['user'] = username
            session['role'] = user['role']
            session['name'] = user['name']
            return jsonify({'success': True, 'role': user['role']})
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def require_login(role=None):
    if 'user' not in session:
        return False
    if role and session.get('role') != role:
        return False
    return True

# ── Pages ──────────────────────────────────────────────────────────────────────
@app.route('/hospital')
def hospital_dashboard():
    if not require_login('hospital'):
        return redirect(url_for('login'))
    return render_template('hospital.html', user_name=session['name'])

@app.route('/treatment')
def treatment_page():
    if not require_login('hospital'):
        return redirect(url_for('login'))
    return render_template('treatment.html', user_name=session['name'])

@app.route('/bill')
def bill_page():
    if not require_login('hospital'):
        return redirect(url_for('login'))
    return render_template('bill.html', user_name=session['name'])

@app.route('/insurance')
def insurance_dashboard():
    if not require_login('insurance'):
        return redirect(url_for('login'))
    return render_template('insurance.html', user_name=session['name'])

@app.route('/discharge')
def discharge_page():
    if not require_login('hospital'):
        return redirect(url_for('login'))
    return render_template('discharge.html', user_name=session['name'])

# ── API ────────────────────────────────────────────────────────────────────────
@app.route('/api/patients', methods=['GET'])
def get_patients():
    return jsonify(list(patients.values()))

@app.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    pid = f'P{patient_counter[0]:03d}'
    patient_counter[0] += 1
    patients[pid] = {
        'id': pid,
        'name': data['name'],
        'age': int(data['age']),
        'insurance_id': data['insurance_id'],
        'diagnosis': data.get('diagnosis', 'Under Observation'),
        'admitted': datetime.now().strftime('%Y-%m-%d'),
        'status': 'admitted',
        'ward': data.get('ward', 'General Ward'),
    }
    treatments[pid] = []
    return jsonify({'success': True, 'patient': patients[pid]})

@app.route('/api/treatments/<pid>', methods=['GET'])
def get_treatments(pid):
    return jsonify(treatments.get(pid, []))

@app.route('/api/treatments/<pid>', methods=['POST'])
def add_treatment(pid):
    data = request.get_json()
    tid = f'T{treatment_counter[0]:03d}'
    treatment_counter[0] += 1
    entry = {
        'id': tid,
        'procedure': data['procedure'],
        'cost': float(data['cost']),
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
        'doctor': data.get('doctor', 'Staff'),
    }
    treatments.setdefault(pid, []).append(entry)
    return jsonify({'success': True, 'treatment': entry})

@app.route('/api/treatments/<pid>/<tid>', methods=['DELETE'])
def delete_treatment(pid, tid):
    if pid in treatments:
        treatments[pid] = [t for t in treatments[pid] if t['id'] != tid]
    return jsonify({'success': True})

@app.route('/api/bills', methods=['GET'])
def get_bills():
    result = []
    for b in bills.values():
        p = patients.get(b['patient_id'], {})
        result.append({**b, 'patient_name': p.get('name',''), 'insurance_id': p.get('insurance_id','')})
    return jsonify(result)

@app.route('/api/bills/<pid>', methods=['GET'])
def get_bill_for_patient(pid):
    for b in bills.values():
        if b['patient_id'] == pid:
            p = patients.get(pid, {})
            return jsonify({**b, 'patient': p, 'treatments': treatments.get(pid, [])})
    return jsonify(None)

@app.route('/api/bills', methods=['POST'])
def submit_bill():
    data = request.get_json()
    pid = data['patient_id']
    # Check if bill already exists
    for b in bills.values():
        if b['patient_id'] == pid:
            b['status'] = 'pending'
            b['total'] = data['total']
            b['submitted_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            return jsonify({'success': True, 'bill': b})
    bid = f'B{bill_counter[0]:03d}'
    bill_counter[0] += 1
    bill = {
        'id': bid, 'patient_id': pid,
        'total': data['total'], 'status': 'pending',
        'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'notes': '', 'reviewed_by': None, 'reviewed_at': None
    }
    bills[bid] = bill
    return jsonify({'success': True, 'bill': bill})

@app.route('/api/bills/<bid>/review', methods=['POST'])
def review_bill(bid):
    data = request.get_json()
    if bid not in bills:
        return jsonify({'success': False, 'message': 'Bill not found'})
    bills[bid]['status'] = data['action']  # 'approved' or 'rejected'
    bills[bid]['notes'] = data.get('notes', '')
    bills[bid]['reviewed_by'] = session.get('name', 'Insurance Officer')
    bills[bid]['reviewed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    return jsonify({'success': True})

@app.route('/api/discharge/<pid>', methods=['POST'])
def discharge_patient(pid):
    bill_approved = any(b['patient_id'] == pid and b['status'] == 'approved' for b in bills.values())
    if not bill_approved:
        return jsonify({'success': False, 'message': 'Insurance approval required'})
    if pid in patients:
        patients[pid]['status'] = 'discharged'
        patients[pid]['discharged_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    return jsonify({'success': True, 'discharged_at': patients[pid]['discharged_at']})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
