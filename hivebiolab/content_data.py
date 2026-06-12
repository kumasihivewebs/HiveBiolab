from __future__ import annotations

from typing import List, Dict

PROJECTS_PAGE_DATA: Dict[str, object] = {
    "title": "Projects",
    "eyebrow": "Open science in practice",
    "description": (
        "Explore Hive Biolab projects across open science hardware, local biotech "
        "capacity building, enzyme manufacturing and hands-on innovation programs."
    ),
    "stats": [
        {"label": "Featured projects", "value": "3"},
        {"label": "Students trained", "value": "200+"},
        {"label": "Partner institutions", "value": "6+"},
    ],
    "filters": ["All", "Open Science", "Innovation"],
}

PROJECTS_DATA: List[Dict[str, object]] = [
    {
        "id": "ecb4osh",
        "title": "ECB4OSH Project",
        "slug": "ecb4osh-project",
        "description": (
            "Building Open Science Capacity Across Africa - The Education and "
            "Capacity Building for Open Science Hardware project led by Africa Open "
            "Science & Hardware (AfricaOSH)."
        ),
        "longDescription": (
            "The Education and Capacity Building for Open Science Hardware (ECB4OSH) "
            "project is a groundbreaking initiative led by Africa Open Science & "
            "Hardware (AfricaOSH), with Hive Biolab and Kumasi Hive as key implementation "
            "partners. The project aimed to make scientific exploration more accessible by "
            "training university students across Ghana to build and use open-source scientific "
            "tools for research, education and innovation."
        ),
        "status": "Completed",
        "category": "Open Science",
        "tags": ["Open Science", "Hardware", "Education", "Capacity Building"],
        "startDate": "2022-01-01",
        "endDate": "2023-12-31",
        "image_key": "osh",
        "gallery": [
            "/api/placeholder/800/600",
            "/api/placeholder/800/600",
            "/api/placeholder/800/600",
        ],
        "team": ["AfricaOSH", "Hive Biolab", "Kumasi Hive"],
        "collaborators": [
            "KNUST",
            "University of Cape Coast",
            "University of Energy and Natural Resources",
        ],
        "funding": "AfricaOSH Initiative",
        "impact": [
            "200+ students trained",
            "OpenFlexure Microscope workshops",
            "Joined AfricaOSH and GOSH communities",
            "Microscopes donated to schools and labs",
        ],
        "route": "/projects/ecb4osh",
        "links": {"website": "https://africaosh.com"},
    },
    {
        "id": "biomaker-challenge",
        "title": "Biomaker Challenge - Ghana",
        "slug": "biomaker-challenge-ghana",
        "description": (
            "Building science hardware for biology - A transformative program in collaboration "
            "with the Open Bioeconomy Lab and the Biomaker Africa network."
        ),
        "longDescription": (
            "The Biomaker Challenge Ghana is a transformative program in collaboration with "
            "the Open Bioeconomy Lab and the Biomaker Africa network. This initiative empowers "
            "students, researchers and young innovators to design and build low-cost open science "
            "hardware for solving real-world challenges in health, agriculture and the environment."
        ),
        "status": "Completed",
        "category": "Innovation",
        "tags": ["Hardware", "Innovation", "Prototyping", "Open Science"],
        "startDate": "2022-01-01",
        "endDate": "2023-12-31",
        "image_key": "bio",
        "gallery": ["/api/placeholder/800/600", "/api/placeholder/800/600"],
        "team": ["Open Bioeconomy Lab", "Biomaker Africa Network"],
        "collaborators": ["Hive Biolab", "Local Universities"],
        "funding": "Open Bioeconomy Lab",
        "impact": [
            "Solar powered power pack for gel electrophoresis",
            "Colorimeter for urine analysis",
            "Water quality sensor for mining areas",
            "Air quality sensor for environmental monitoring",
            "Smart DIY biological safety cabinet",
        ],
        "route": "/projects/biomaker-challenge",
        "links": {"website": "https://biomaker.org"},
    },
    {
        "id": "open-enzyme-manufacturing",
        "title": "Open Enzyme Manufacturing",
        "slug": "open-enzyme-manufacturing",
        "description": (
            "Building Local Capacity for Enzyme Production in Ghana - A week-long hands-on "
            "program designed to equip young scientists with practical skills in local DNA "
            "polymerase enzyme production."
        ),
        "longDescription": (
            "The Open Enzyme Manufacturing Masterclass was piloted in Ghana through a collaboration "
            "between Hive Biolab, KNUST and the Open Bioeconomy Lab. This week-long hands-on program "
            "was designed to equip young scientists and early-career researchers with practical skills "
            "in the local production of DNA polymerase enzymes for use in molecular biology and "
            "diagnostic applications."
        ),
        "status": "Completed",
        "category": "Open Science",
        "tags": ["Enzymes", "Manufacturing", "Training", "Local Production"],
        "startDate": "2023-01-01",
        "endDate": "2023-12-31",
        "image_key": "enzyme",
        "gallery": ["/api/placeholder/800/600", "/api/placeholder/800/600"],
        "team": ["Hive Biolab", "KNUST", "Open Bioeconomy Lab"],
        "collaborators": ["Open Bioeconomy Lab Global Network"],
        "funding": "Open Bioeconomy Lab",
        "impact": [
            "12 participants trained",
            "Complete enzyme production pipeline training",
            "Successful OpenVent DNA polymerase expression",
            "Strengthened regional biotech capacity",
        ],
        "route": "/projects/open-enzyme-manufacturing",
        "links": {"website": "https://openbioeconomy.org"},
    },
]

TRAINING_PROGRAMS_DATA: List[Dict[str, object]] = [
    {
        "id": "training-microbiology",
        "slug": "microbiology",
        "title": "Microbiology Training",
        "description": (
            "Essential aseptic techniques, culturing, sampling, media preparation, staining and "
            "biochemical tests for environmental, food and health research."
        ),
        "level": "Beginner",
        "color": "from-biolab-teal-500 to-biolab-teal-600",
        "image_key": "micro",
        "icon_name": "microscope",
        "route": "/training/microbiology",
        "details": {
            "overview": (
                "Comprehensive microbiology training covering essential laboratory techniques for "
                "environmental, food, and health research applications. This hands-on program provides "
                "participants with fundamental skills in microbiological analysis and sterile laboratory "
                "practices."
            ),
            "curriculum": [
                "Aseptic techniques and laboratory safety protocols",
                "Media preparation and sterilization methods",
                "Bacterial culturing and isolation techniques",
                "Staining procedures and microscopy",
                "Biochemical identification tests",
                "Quality control and contamination prevention",
                "Environmental sampling techniques",
                "Food microbiology applications",
                "Health-related microbiological testing",
            ],
            "prerequisites": (
                "Basic science background preferred but not required. High school biology knowledge helpful."
            ),
            "outcomes": (
                "Participants will be able to perform standard microbiological analyses, maintain sterile "
                "laboratory conditions, and conduct environmental and food safety testing."
            ),
            "duration": "4 weeks intensive program",
            "format": "Hands-on laboratory sessions with theoretical components",
            "certification": "Certificate of Completion in Microbiology Techniques",
        },
    },
    {
        "id": "training-molecular-biology",
        "slug": "molecular-biology",
        "title": "Molecular Biology & Genetic Engineering",
        "description": (
            "DNA extraction, PCR, gel electrophoresis, plasmid design and gene expression analysis for "
            "modern biotechnology applications."
        ),
        "level": "Intermediate",
        "color": "from-biolab-purple-500 to-biolab-purple-600",
        "image_key": "molecular engineering",
        "icon_name": "dna",
        "route": "/training/molecular-biology",
        "details": {
            "overview": (
                "Molecular biology training focusing on DNA manipulation, PCR techniques, and genetic "
                "engineering applications. This program prepares participants for biotechnology research "
                "and applications."
            ),
            "curriculum": [
                "DNA/RNA extraction and purification techniques",
                "PCR amplification and optimization strategies",
                "Gel electrophoresis and molecular analysis",
                "Plasmid design and molecular cloning",
                "Gene expression analysis and regulation",
                "Genetic engineering principles and applications",
                "Recombinant DNA technology",
                "Protein expression and purification",
                "Modern biotechnology applications",
            ],
            "prerequisites": (
                "Basic molecular biology knowledge or completion of microbiology training. University-level "
                "biology background recommended."
            ),
            "outcomes": (
                "Participants will master molecular techniques essential for modern biotechnology research, "
                "genetic engineering, and diagnostic applications."
            ),
            "duration": "3 weeks program",
            "format": "Laboratory-intensive with project-based learning",
            "certification": "Certificate in Molecular Biology & Genetic Engineering",
        },
    },
    {
        "id": "training-bioinformatics",
        "slug": "bioinformatics",
        "title": "Bioinformatics & Data Analysis",
        "description": (
            "DNA sequence analysis, antimicrobial resistance tracking, blending coding and biology to solve "
            "modern health challenges."
        ),
        "level": "Intermediate",
        "color": "from-biolab-amber-500 to-biolab-amber-600",
        "image_key": "informatics",
        "icon_name": "bar-chart",
        "route": "/training/bioinformatics",
        "details": {
            "overview": (
                "Computational biology training combining programming skills with biological data analysis for "
                "modern research applications. Learn to analyze genomic data and solve health challenges using "
                "bioinformatics tools."
            ),
            "curriculum": [
                "Introduction to bioinformatics and computational biology",
                "DNA and protein sequence analysis",
                "Phylogenetic analysis and evolutionary studies",
                "Genome assembly and annotation",
                "Data visualization and statistical analysis",
                "Antimicrobial resistance tracking systems",
                "Programming for biologists (Python/R)",
                "Database management and mining",
                "Machine learning applications in biology",
            ],
            "prerequisites": (
                "Basic computer skills and biology background. Programming experience helpful but not required."
            ),
            "outcomes": (
                "Participants will be able to analyze biological data computationally, develop bioinformatics "
                "pipelines, and solve health challenges using computational approaches."
            ),
            "duration": "4 weeks program",
            "format": "Computer lab sessions with practical projects",
            "certification": "Certificate in Bioinformatics & Computational Biology",
        },
    },
    {
        "id": "training-synthetic-biology",
        "slug": "synthetic-biology",
        "title": "Synthetic Biology & Biomaker",
        "description": (
            "Design biotech solutions using open-source tools, DIY lab equipment and local materials for sustainable innovation."
        ),
        "level": "Advanced",
        "color": "from-biolab-teal-400 to-biolab-purple-500",
        "image_key": "synthetic",
        "icon_name": "cpu",
        "route": "/training/synthetic-biology",
        "details": {
            "overview": (
                "Cutting-edge synthetic biology training focusing on designing biological systems and building "
                "biotech solutions using open-source tools. Learn to create innovative solutions for local "
                "challenges using sustainable approaches."
            ),
            "curriculum": [
                "Synthetic biology principles and design thinking",
                "Biodesign methodologies and frameworks",
                "DIY laboratory equipment construction",
                "Open-source tool utilization and modification",
                "Biosafety protocols and ethical considerations",
                "Project development and prototyping",
                "Sustainable biotechnology approaches",
                "Community-based innovation strategies",
                "Entrepreneurship in biotechnology",
            ],
            "prerequisites": (
                "Molecular biology background and programming experience preferred. Strong problem-solving skills essential."
            ),
            "outcomes": (
                "Participants will be able to design and build biological systems for sustainable innovation, create DIY lab equipment, and develop community-based biotechnology solutions."
            ),
            "duration": "5 weeks immersive lab training",
            "format": "Workshop-style with hands-on building and design",
            "certification": "Certificate in Synthetic Biology & Biomaker Innovation",
        },
    },
]

TRAINING_PAGE_DATA: Dict[str, object] = {
    "title": "Training",
    "eyebrow": "Practical biotech education",
    "description": (
        "Hands-on programs for students, researchers and innovators who want to "
        "build practical capacity in microbiology, molecular biology, "
        "bioinformatics and synthetic biology."
    ),
    "stats": [
        {"label": "Training tracks", "value": "4"},
        {"label": "Learning mode", "value": "Hands-on"},
        {"label": "Certificates", "value": "Available"},
    ],
    "applicationSteps": [
        "Choose the training track that matches your goals.",
        "Submit your contact details, background and learning objectives.",
        "Hive Biolab follows up with cohort timing, requirements and next steps.",
    ],
}

CONTACT_PAGE_DATA: Dict[str, object] = {
    "title": "Contact",
    "eyebrow": "Work with Hive Biolab",
    "description": (
        "Reach out for training inquiries, research collaborations, lab access, "
        "open science partnerships and community biotechnology programs."
    ),
    "contact": {
        "email": "biolab@kumasihive.com",
        "location": "Kumasi Hive, Kumasi, Ghana",
        "responseTime": "We typically respond within 2 business days.",
    },
    "inquiryTypes": [
        "Training inquiry",
        "Research collaboration",
        "Lab access",
        "Open science partnership",
        "General inquiry",
    ],
}
