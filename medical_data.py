# medical_data.py

SAMPLE_DISEASES = [
    {
        "id": "d1",
        "name": "Ischemic Heart Disease",
        "category": "Cardiovascular",
        "short_desc": "Coronary artery disease; chest pain, dyspnea.",
        "key_symptoms": ["chest pain", "shortness of breath", "sweating"],
        "primary_drugs": ["Aspirin", "Nitroglycerin"],
        "risk_factors": ["hypertension", "smoking"]
    },
    {
        "id": "d2",
        "name": "Community-Acquired Pneumonia",
        "category": "Respiratory",
        "short_desc": "Infection of lung tissue; cough, fever.",
        "key_symptoms": ["fever", "cough", "shortness of breath"],
        "primary_drugs": ["Amoxicillin", "Azithromycin"],
        "risk_factors": ["age>65", "smoking"]
    },
    {
        "id": "d3",
        "name": "Ischemic Stroke",
        "category": "Neurological",
        "short_desc": "Acute neurological deficit; weakness, slurred speech.",
        "key_symptoms": ["weakness", "facial droop", "speech difficulty"],
        "primary_drugs": ["Aspirin", "tPA (select)"],
        "risk_factors": ["hypertension", "atrial fibrillation"]
    },
]

# Updated with data extracted from Essential Medicine List PDFs and Google Search
SAMPLE_DRUGS = [
    # --- Section 1: Anesthetic Agents ---
    {
        "name": "Halothane",
        "class": "General Anesthetic",
        "indications": "General Anesthesia induction and maintenance",
        "common_side_effects": "Shivering, nausea, vomiting; rare but severe liver damage (hepatitis), malignant hyperthermia",
        "major_interactions": "Adrenaline (arrhythmias), other CNS depressants",
        "contraindications": "History of malignant hyperthermia, history of unexplained jaundice/fever after previous exposure"
    },
    {
        "name": "Ketamine",
        "class": "General Anesthetic",
        "indications": "Anesthesia (diagnostic/surgical), analgesia",
        "common_side_effects": "Hallucinations, vivid dreams (emergence reactions), increased blood pressure/heart rate, respiratory depression (rare)",
        "major_interactions": "Benzodiazepines (prolonged recovery), Thyroid hormones (hypertension), CNS depressants",
        "contraindications": "Hypertension (severe), eclampsia, history of stroke"
    },
    {
        "name": "Propofol",
        "class": "General Anesthetic",
        "indications": "Induction/maintenance of anesthesia, sedation in ICU",
        "common_side_effects": "Hypotension (low blood pressure), apnea (stopped breathing), injection site pain, propofol infusion syndrome (rare)",
        "major_interactions": "Opioids, benzodiazepines (additive cardiorespiratory depression)",
        "contraindications": "Hypersensitivity to eggs, egg products, soybeans, or soy products"
    },
    {
        "name": "Lignocaine",
        "class": "Local Anesthetic / Antiarrhythmic",
        "indications": "Local anesthesia (infiltration, block), ventricular arrhythmias",
        "common_side_effects": "Dizziness, tinnitus, blurred vision, bradycardia, hypotension; seizures (toxicity)",
        "major_interactions": "Beta-blockers (increased toxicity), Amiodarone, Propofol (additive effects)",
        "contraindications": "Severe heart block, hypovolemia"
    },
    {
        "name": "Atropine",
        "class": "Anticholinergic / Antidote",
        "indications": "Preoperative sedation (drying secretions), organophosphorus poisoning, bradycardia",
        "common_side_effects": "Dry mouth, blurred vision, photophobia, tachycardia, constipation, urinary retention",
        "major_interactions": "Antihistamines, TCAs, Antipsychotics (additive anticholinergic effects)",
        "contraindications": "Glaucoma (angle-closure), pyloric stenosis, prostatic hypertrophy"
    },

    # --- Section 2: Analgesics, Antipyretics, NSAIDs ---
    {
        "name": "Acetylsalicylic acid",
        "class": "Analgesic / Antiplatelet",
        "indications": "Pain, fever, inflammation, prevention of MI/stroke",
        "common_side_effects": "GI irritation, bleeding, tinnitus, bronchospasm",
        "major_interactions": "Warfarin/Heparin (bleeding), Methotrexate (toxicity), Steroids (GI ulcers)",
        "contraindications": "Active peptic ulcer, bleeding disorders, aspirin-induced asthma, children <16 yrs (Reye's syndrome)"
    },
    {
        "name": "Diclofenac",
        "class": "NSAID",
        "indications": "Rheumatoid arthritis, osteoarthritis, acute pain, inflammation",
        "common_side_effects": "GI ulcers/bleeding, cardiovascular events (MI/stroke risk), renal impairment, fluid retention",
        "major_interactions": "Aspirin, Warfarin, ACE inhibitors (renal failure), Lithium",
        "contraindications": "Active GI bleeding, severe heart failure, history of asthma/urticaria after NSAIDs, pregnancy (>20 weeks)"
    },
    {
        "name": "Paracetamol",
        "class": "Analgesic / Antipyretic",
        "indications": "Mild to moderate pain, fever",
        "common_side_effects": "Rare; hepatotoxicity (liver damage) in overdose, skin rash",
        "major_interactions": "Warfarin (prolonged use), Carbamazepine (enzyme induction), Alcohol",
        "contraindications": "Severe liver disease/failure"
    },
    {
        "name": "Morphine",
        "class": "Opioid Analgesic",
        "indications": "Severe pain, palliative care",
        "common_side_effects": "Respiratory depression, constipation, nausea/vomiting, sedation, hypotension",
        "major_interactions": "CNS depressants (benzodiazepines, alcohol), MAOIs",
        "contraindications": "Acute respiratory depression, paralytic ileus, raised intracranial pressure"
    },
    {
        "name": "Allopurinol",
        "class": "Antigout",
        "indications": "Chronic gout, hyperuricemia",
        "common_side_effects": "Rash (can be severe - SJS), nausea, acute gout flares (initiation)",
        "major_interactions": "Azathioprine/Mercaptopurine (severe toxicity), Amoxicillin (rash risk)",
        "contraindications": "Hypersensitivity"
    },

    # --- Section 3: Antiallergics ---
    {
        "name": "Adrenaline",
        "class": "Sympathomimetic",
        "indications": "Anaphylaxis, cardiac arrest, severe asthma",
        "common_side_effects": "Tachycardia, palpitations, anxiety, tremor, hypertension",
        "major_interactions": "Beta-blockers (hypertension), TCAs, MAOIs",
        "contraindications": "None in life-threatening emergency; caution in ischemic heart disease"
    },
    {
        "name": "Cetirizine",
        "class": "Antihistamine",
        "indications": "Allergic rhinitis, urticaria",
        "common_side_effects": "Drowsiness, dry mouth, fatigue, dizziness",
        "major_interactions": "CNS depressants, Alcohol",
        "contraindications": "Severe renal impairment (end-stage renal disease)"
    },
    {
        "name": "Dexamethasone",
        "class": "Corticosteroid",
        "indications": "Severe inflammation, allergic conditions, cerebral edema, COVID-19",
        "common_side_effects": "Hyperglycemia, insomnia, fluid retention, mood changes, increased infection risk",
        "major_interactions": "NSAIDs (GI ulcers), Vaccines (reduced efficacy), CYP3A4 inducers",
        "contraindications": "Systemic fungal infections, live vaccines (high dose)"
    },

    # --- Section 5: Anticonvulsants ---
    {
        "name": "Carbamazepine",
        "class": "Anticonvulsant",
        "indications": "Epilepsy (partial/tonic-clonic), trigeminal neuralgia, bipolar disorder",
        "common_side_effects": "Dizziness, drowsiness, ataxia, nausea, skin rash (SJS/TEN risk), agranulocytosis (rare)",
        "major_interactions": "Warfarin, Oral Contraceptives (reduced effect), MAOIs, Erythromycin",
        "contraindications": "Bone marrow depression, hepatic porphyrias, AV block"
    },
    {
        "name": "Diazepam",
        "class": "Benzodiazepine",
        "indications": "Anxiety, muscle spasms, seizures (status epilepticus), alcohol withdrawal",
        "common_side_effects": "Sedation, drowsiness, muscle weakness, respiratory depression, dependence",
        "major_interactions": "Opioids (risk of coma/death), Alcohol, CNS depressants",
        "contraindications": "Severe respiratory insufficiency, sleep apnea, myasthenia gravis"
    },
    {
        "name": "Sodium valproate",
        "class": "Anticonvulsant",
        "indications": "Epilepsy (generalized/partial), bipolar disorder",
        "common_side_effects": "Nausea, weight gain, tremor, hair loss, liver toxicity, pancreatitis",
        "major_interactions": "Lamotrigine (rash risk), Carbamazepine, Aspirin",
        "contraindications": "Liver disease, Pregnancy (highly teratogenic), mitochondrial disorders"
    },

    # --- Section 6: Anti-infective Medicines ---
    {
        "name": "Albendazole",
        "class": "Anthelmintic",
        "indications": "Intestinal worms (neurocysticercosis, hydatid disease)",
        "common_side_effects": "Headache, liver enzyme elevation, abdominal pain, nausea/vomiting",
        "major_interactions": "Dexamethasone (increases albendazole levels), Cimetidine",
        "contraindications": "Hypersensitivity, pregnancy (caution)"
    },
    {
        "name": "Amoxicillin",
        "class": "Antibiotic (Penicillin)",
        "indications": "Respiratory tract infections, UTI, H. pylori",
        "common_side_effects": "Diarrhea, nausea, skin rash, yeast infections",
        "major_interactions": "Allopurinol (rash), Methotrexate (toxicity), Oral contraceptives",
        "contraindications": "Hypersensitivity to penicillins"
    },
    {
        "name": "Ceftriaxone",
        "class": "Antibiotic (Cephalosporin)",
        "indications": "Meningitis, pneumonia, gonorrhea, sepsis",
        "common_side_effects": "Diarrhea, injection site pain, rash, biliary sludge (pseudolithiasis)",
        "major_interactions": "Calcium-containing IV solutions (precipitation risk), Warfarin",
        "contraindications": "Hypersensitivity to cephalosporins, neonates with hyperbilirubinemia"
    },
    {
        "name": "Azithromycin",
        "class": "Antibiotic (Macrolide)",
        "indications": "Respiratory infections, STIs",
        "common_side_effects": "Diarrhea, nausea, abdominal pain",
        "major_interactions": "QT prolonging drugs, Warfarin, Digoxin",
        "contraindications": "Hypersensitivity to macrolides, history of cholestatic jaundice with use"
    },
    {
        "name": "Ciprofloxacin",
        "class": "Antibiotic (Fluoroquinolone)",
        "indications": "UTI, typhoid, respiratory infections",
        "common_side_effects": "Nausea, diarrhea, tendonitis/tendon rupture, CNS effects (dizziness/seizures)",
        "major_interactions": "Theophylline, Warfarin, Tizanidine, Antacids (reduced absorption)",
        "contraindications": "History of tendon disorders, Myasthenia gravis (exacerbation)"
    },
    {
        "name": "Metronidazole",
        "class": "Antibiotic / Antiprotozoal",
        "indications": "Anaerobic infections, amoebiasis, giardiasis, trichomoniasis",
        "common_side_effects": "Metallic taste, nausea, abdominal cramps, headache, dark urine",
        "major_interactions": "Alcohol (disulfiram-like reaction), Warfarin, Lithium",
        "contraindications": "Hypersensitivity, first trimester of pregnancy (high dose)"
    },
    {
        "name": "Rifampicin",
        "class": "Antitubercular",
        "indications": "Tuberculosis, Leprosy",
        "common_side_effects": "Red/orange discoloration of body fluids, hepatotoxicity, flu-like syndrome",
        "major_interactions": "Potent CYP inducer (reduces effect of OCPs, ARTs, Warfarin, Steroids)",
        "contraindications": "Jaundice, hypersensitivity"
    },
    {
        "name": "Fluconazole",
        "class": "Antifungal",
        "indications": "Candidiasis (thrush, vaginal, systemic), cryptococcal meningitis",
        "common_side_effects": "Nausea, headache, abdominal pain, diarrhea, rash",
        "major_interactions": "QT prolonging drugs, Warfarin, Phenytoin, Rifampicin",
        "contraindications": "Co-administration with terfenadine or cisapride"
    },
    {
        "name": "Acyclovir",
        "class": "Antiviral",
        "indications": "Herpes simplex, Varicella zoster (chickenpox/shingles)",
        "common_side_effects": "Nausea, vomiting, diarrhea, headache; renal impairment (IV)",
        "major_interactions": "Nephrotoxic drugs, Probenecid",
        "contraindications": "Hypersensitivity"
    },
    {
        "name": "Chloroquine",
        "class": "Antimalarial / DMARD",
        "indications": "Malaria treatment/prophylaxis, Rheumatoid arthritis",
        "common_side_effects": "Nausea, headache, visual disturbances (retinopathy), itching",
        "major_interactions": "Amiodarone (arrhythmia risk), Antacids, Cimetidine",
        "contraindications": "Retinal or visual field changes, psoriasis exacerbation"
    },

    # --- Section 10: Medicines affecting blood ---
    {
        "name": "Ferrous salts",
        "class": "Antianaemia",
        "indications": "Iron deficiency anaemia",
        "common_side_effects": "GI upset, constipation, black stools, nausea",
        "major_interactions": "Antacids, Tetracyclines, Levothyroxine (reduced absorption)",
        "contraindications": "Hemochromatosis, hemolytic anemia"
    },
    {
        "name": "Heparin",
        "class": "Anticoagulant",
        "indications": "DVT/PE treatment and prophylaxis, ACS",
        "common_side_effects": "Bleeding, thrombocytopenia (HIT), injection site reactions",
        "major_interactions": "Aspirin, NSAIDs, Warfarin (bleeding risk)",
        "contraindications": "Active bleeding, severe thrombocytopenia"
    },

    # --- Section 12: Cardiovascular Medicines ---
    {
        "name": "Amlodipine",
        "class": "Antihypertensive (Calcium Channel Blocker)",
        "indications": "Hypertension, Angina",
        "common_side_effects": "Peripheral edema (swelling ankles), flushing, palpitations, dizziness",
        "major_interactions": "Simvastatin (limit dose), CYP3A4 inhibitors",
        "contraindications": "Severe hypotension, cardiogenic shock"
    },
    {
        "name": "Atenolol",
        "class": "Antihypertensive (Beta-blocker)",
        "indications": "Hypertension, Angina, Arrhythmias",
        "common_side_effects": "Bradycardia, cold extremities, fatigue, dizziness",
        "major_interactions": "Verapamil/Diltiazem (heart block), NSAIDs (reduced effect)",
        "contraindications": "Asthma (caution), second/third-degree heart block, severe heart failure"
    },
    {
        "name": "Enalapril",
        "class": "Antihypertensive (ACE Inhibitor)",
        "indications": "Hypertension, Heart failure",
        "common_side_effects": "Dry cough, hypotension, hyperkalemia, dizziness, angioedema",
        "major_interactions": "Potassium supplements/sparing diuretics, NSAIDs, Lithium",
        "contraindications": "History of angioedema, pregnancy, bilateral renal artery stenosis"
    },
    {
        "name": "Glyceryl trinitrate",
        "class": "Antianginal",
        "indications": "Angina pectoris, Heart failure",
        "common_side_effects": "Headache (severe), flushing, hypotension, dizziness, tachycardia",
        "major_interactions": "PDE5 inhibitors (Sildenafil - severe hypotension), Alcohol",
        "contraindications": "Severe anemia, raised intracranial pressure, hypotension"
    },
    {
        "name": "Atorvastatin",
        "class": "Hypolipidemic (Statin)",
        "indications": "Hypercholesterolemia, CV risk reduction",
        "common_side_effects": "Myalgia (muscle pain), GI disturbance, headache, liver enzyme elevation",
        "major_interactions": "CYP3A4 inhibitors (macrolides, antifungals), Gemfibrozil (rhabdomyolysis)",
        "contraindications": "Active liver disease, pregnancy, breastfeeding"
    },
    {
        "name": "Digoxin",
        "class": "Cardiac Glycoside",
        "indications": "Heart failure, Atrial fibrillation",
        "common_side_effects": "Nausea, vomiting, visual disturbances (halos), arrhythmias",
        "major_interactions": "Amiodarone, Verapamil, Diuretics (hypokalemia risk)",
        "contraindications": "Ventricular fibrillation, toxicity history"
    },

    # --- Section 14: Dermatological Medicines ---
    {
        "name": "Clotrimazole",
        "class": "Antifungal",
        "indications": "Fungal skin infections (tinea), candidiasis",
        "common_side_effects": "Local irritation, stinging, burning, erythema",
        "major_interactions": "Minimal systemic absorption; latex condoms (damage)",
        "contraindications": "Hypersensitivity"
    },
    {
        "name": "Silver sulphadiazine",
        "class": "Antibacterial",
        "indications": "Prevention/treatment of infection in burns",
        "common_side_effects": "Burning sensation, itching, transient leukopenia, skin discoloration",
        "major_interactions": "Cimetidine (rare), proteolytic enzymes (inactivation)",
        "contraindications": "Hypersensitivity to sulfonamides, pregnancy near term, premature infants"
    },
    {
        "name": "Betamethasone",
        "class": "Corticosteroid (Topical)",
        "indications": "Eczema, psoriasis, inflammatory skin conditions",
        "common_side_effects": "Skin atrophy (thinning), striae, burning, folliculitis",
        "major_interactions": "None significant for topical use",
        "contraindications": "Untreated bacterial/viral/fungal skin infections, rosacea"
    },

    # --- Section 18: Diuretics ---
    {
        "name": "Furosemide",
        "class": "Loop Diuretic",
        "indications": "Edema (Heart failure, renal/hepatic disease), Hypertension",
        "common_side_effects": "Dehydration, hypotension, hypokalemia, hyponatremia, gout",
        "major_interactions": "Aminoglycosides (ototoxicity), Lithium (toxicity), NSAIDs",
        "contraindications": "Anuria, severe electrolyte depletion"
    },

    # --- Section 20: Gastrointestinal Medicines ---
    {
        "name": "Omeprazole",
        "class": "Proton Pump Inhibitor (PPI)",
        "indications": "GERD, Peptic ulcer disease, H. pylori eradication",
        "common_side_effects": "Headache, abdominal pain, diarrhea, nausea",
        "major_interactions": "Clopidogrel (reduced effect), Levothyroxine, Methotrexate",
        "contraindications": "Hypersensitivity"
    },
    {
        "name": "Ranitidine",
        "class": "H2 Receptor Antagonist",
        "indications": "Gastric ulcers, GERD, heartburn",
        "common_side_effects": "Headache, diarrhea/constipation, dizziness",
        "major_interactions": "May alter absorption of pH-dependent drugs (Ketoconazole)",
        "contraindications": "Hypersensitivity"
    },
    {
        "name": "Domperidone",
        "class": "Antiemetic / Prokinetic",
        "indications": "Nausea, vomiting, gastroparesis",
        "common_side_effects": "Dry mouth, headache; serious: QT prolongation, arrhythmias",
        "major_interactions": "QT prolonging drugs (Erythromycin, Ketoconazole), anticholinergics",
        "contraindications": "GI hemorrhage/obstruction, moderate/severe liver impairment, cardiac disease (QT issues)"
    },
    {
        "name": "Oral rehydration salts",
        "class": "Electrolyte Replenisher",
        "indications": "Dehydration from diarrhea/vomiting",
        "common_side_effects": "Vomiting (if taken too fast), hypernatremia (if mixed incorrectly)",
        "major_interactions": "None significant",
        "contraindications": "Severe dehydration requiring IV, intestinal obstruction, intractable vomiting"
    },

    # --- Section 21: Hormones and Endocrine ---
    {
        "name": "Prednisolone",
        "class": "Corticosteroid",
        "indications": "Allergy, asthma, autoimmune diseases, inflammation",
        "common_side_effects": "Fluid retention, weight gain, hypertension, hyperglycemia, osteoporosis (long term)",
        "major_interactions": "NSAIDs, Antidiabetics (reduced effect), Vaccines",
        "contraindications": "Systemic fungal infections"
    },
    {
        "name": "Insulin (Soluble)",
        "class": "Antidiabetic",
        "indications": "Diabetes Mellitus, Hyperkalemia",
        "common_side_effects": "Hypoglycemia (sweating, tremor, confusion), injection site reactions, weight gain",
        "major_interactions": "Beta-blockers (mask hypoglycemia), Steroids (hyperglycemia), Alcohol",
        "contraindications": "Hypoglycemia"
    },
    {
        "name": "Metformin",
        "class": "Antidiabetic",
        "indications": "Type 2 Diabetes Mellitus",
        "common_side_effects": "GI disturbance (diarrhea, nausea), metallic taste; Lactic acidosis (rare but serious)",
        "major_interactions": "Iodinated contrast media (renal risk), Alcohol",
        "contraindications": "Severe renal impairment (eGFR <30), acute metabolic acidosis"
    },
    {
        "name": "Levothyroxine",
        "class": "Thyroid Hormone",
        "indications": "Hypothyroidism, TSH suppression in thyroid cancer",
        "common_side_effects": "Palpitations, tachycardia, heat intolerance, weight loss (signs of hyperthyroidism)",
        "major_interactions": "Calcium, Iron, Antacids (reduce absorption - separate by 4 hrs), Warfarin",
        "contraindications": "Untreated adrenal insufficiency, uncorrected thyrotoxicosis, recent MI"
    },

    # --- Section 27: Psychotherapeutic Medicines ---
    {
        "name": "Haloperidol",
        "class": "Antipsychotic",
        "indications": "Schizophrenia, acute psychosis, tics",
        "common_side_effects": "Extrapyramidal symptoms (tremor, stiffness), sedation, QT prolongation",
        "major_interactions": "CNS depressants, Levodopa, QT prolonging drugs",
        "contraindications": "Comatose states, CNS depression, Parkinson's disease"
    },
    {
        "name": "Amitriptyline",
        "class": "Antidepressant (TCA)",
        "indications": "Depression, neuropathic pain, migraine prophylaxis",
        "common_side_effects": "Dry mouth, sedation, constipation, blurred vision, orthostatic hypotension",
        "major_interactions": "MAOIs (hypertensive crisis), SSRIs, Anticholinergics",
        "contraindications": "Recent MI, arrhythmias, mania, severe liver disease"
    },
    {
        "name": "Fluoxetine",
        "class": "Antidepressant (SSRI)",
        "indications": "Depression, OCD, Bulimia, Panic disorder",
        "common_side_effects": "Insomnia, nausea, diarrhea, sexual dysfunction, anxiety",
        "major_interactions": "MAOIs, Tamoxifen, NSAIDs (bleeding), QT prolonging drugs",
        "contraindications": "Use with MAOIs"
    },

    # --- Section 28: Respiratory Tract ---
    {
        "name": "Salbutamol",
        "class": "Bronchodilator (Beta2-agonist)",
        "indications": "Asthma, COPD (bronchospasm)",
        "common_side_effects": "Tremor, tachycardia, palpitations, headache, hypokalemia (high dose)",
        "major_interactions": "Beta-blockers (antagonism), Diuretics (hypokalemia risk)",
        "contraindications": "Hypersensitivity"
    },
    {
        "name": "Budesonide",
        "class": "Corticosteroid (Inhaled)",
        "indications": "Asthma maintenance, COPD",
        "common_side_effects": "Oral candidiasis (thrush), hoarseness, cough",
        "major_interactions": "Strong CYP3A4 inhibitors (Ketoconazole) increase systemic exposure",
        "contraindications": "Status asthmaticus (acute episodes)"
    }
]