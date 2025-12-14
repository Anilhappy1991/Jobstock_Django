from django.templatetags.static import static
# App/context_processors.py

# ctrs data

def global_ctrs(request):
    ctrs = [
        {
            'title' : 'Active Jobs',
            'price' : '200',
            'symbol' : 'M',
        },
        {
            'title' : 'Startups',
            'price' : '40',
            'symbol' : 'K',
        },
        {
            'title' : 'Talents',
            'price' : '340',
            'symbol' : 'K',
        }
    ]
    return {"ctrs": ctrs}


# companies data

def global_companies(request):
    companies = [
        {
            'img' : static('app/img/brand/layar-primary.svg'), 
        },
        {
            'img' : static('app/img/brand/mailchimp-primary.svg'), 
        },
        {
            'img' : static('app/img/brand/fitbit-primary.svg'), 
        },
        {
            'img' : static('app/img/brand/capsule-primary.svg'), 
        },
        {
            'img' : static('app/img/brand/vidados-primary.svg'), 
        }
    ]
    return {"companies": companies}


# jobs data

def global_jobs(request):
    jobs = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '6 Open', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$6K - $10K', 
            'open' : '4 Open', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '3 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$4.2K - $6K', 
            'open' : '2 Open', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$4K - $5.5K', 
            'open' : '5 Open', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$2K - $4K', 
            'open' : '4 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $6K', 
            'open' : '3 Open', 
            'tag' : 'FullTime',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$3.2K - $5K', 
            'open' : '5 Open', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        }
    ]
    return {"jobs": jobs}


# categories data

def global_categories(request):
    categories = [
        {
            'icon' : 'fa-solid fa-file-invoice',
            'title' : 'Accounting & Finance',
            'jobs' : '122 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-caravan',
            'title' : 'Automotive Jobs',
            'jobs' : '78 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-person-chalkboard',
            'title' : 'Business & Tech',
            'jobs' : '25 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-user-graduate',
            'title' : 'Education Training',
            'jobs' : '212 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-briefcase-medical',
            'title' : 'Healthcare',
            'jobs' : '90 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-burger',
            'title' : 'Restaurant & Food',
            'jobs' : '65 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-jet-fighter',
            'title' : 'Transportation',
            'jobs' : '160 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-mobile-screen-button',
            'title' : 'Telecommunications',
            'jobs' : '80 Active Jobs',
        }
    ]
    return {"categories": categories}


# reviews data

def global_reviews(request):
    reviews = [
        {
            'img' : static('app/img/team-1.jpg'),
            'name' : 'Lucia E. Nugent',
            'tag' : 'CEO of Climber',
            'title' : '"The best useful website"',
            'desc' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim.',
        },
        {
            'img' : static('app/img/team-2.jpg'),
            'name' : 'Brenda R. Smith',
            'tag' : 'Founder of Yeloower',
            'title' : '"Ranking is the #1"',
            'desc' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim.',
        },
        {
            'img' : static('app/img/team-3.jpg'),
            'name' : 'Brian B. Wilkerson',
            'tag' : 'CEO of Mark Soft',
            'title' : '"The website is eco friendly"',
            'desc' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim.',
        },
        {
            'img' : static('app/img/team-4.jpg'),
            'name' : 'Miguel L. Benbow',
            'tag' : 'Founder of Mitche LTD',
            'title' : '"100% save and secure website"',
            'desc' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim.',
        },
        {
            'img' : static('app/img/team-5.jpg'),
            'name' : 'Hilda A. Sheppard',
            'tag' : 'CEO of Doodle',
            'title' : '"Very developer friendly website"',
            'desc' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim.',
        }
    ]
    return {"reviews": reviews}


# companies2 data

def global_companies2(request):
    companies2 = [
        {
            'img' : static('app/img/brand/layar-white.svg'), 
        },
        {
            'img' : static('app/img/brand/mailchimp-white.svg'), 
        },
        {
            'img' : static('app/img/brand/forbes-white.svg'), 
        },
        {
            'img' : static('app/img/brand/fitbit-white.svg'), 
        },
        {
            'img' : static('app/img/brand/vidados-white.svg'), 
        }
    ]
    return {"companies2": companies2}


# jobs2 data

def global_jobs2(request):
    jobs2 = [
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'app' : 'Shopify',
            'location' : 'London, UK',
            'price' : '$80K - 110K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'app' : 'Deezroo',
            'location' : 'Canada, USA',
            'price' : '$50K - 70K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'app' : 'Photoshop',
            'location' : 'Denver, USA',
            'price' : '$80K - 90K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'app' : 'Firefox',
            'location' : 'California, USA',
            'price' : '$90K - 100K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'app' : 'Air BNB',
            'location' : 'Canada, USA',
            'price' : '$80K - 110K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'app' : 'Snapchat',
            'location' : 'London, UK',
            'price' : '$60K - 90K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'app' : 'Dribbble',
            'location' : 'New York, USA',
            'price' : '$85K - 90K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'app' : 'Skype',
            'location' : 'Denver, USA',
            'price' : '$70K - 95K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'app' : 'Deezroo',
            'location' : 'Canada, USA',
            'price' : '$50K - 70K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'app' : 'Shopify',
            'location' : 'London, UK',
            'price' : '$80K - 110K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'app' : 'Dribbble',
            'location' : 'New York, USA',
            'price' : '$85K - 90K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'app' : 'Skype',
            'location' : 'Denver, USA',
            'price' : '$70K - 95K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        }
    ]
    return {"jobs2": jobs2}


# needs data

def global_needs(request):
    needs = [
        {
            'number' : '01.',
            'title' : 'Create An Account',
            'desc' : "Post A Job To Tell Us About Your Project. We'll Quickly Match You With The Right Freelancers Find Place Best. Nor again is there anyone who loves.",
        },
        {
            'number' : '02.',
            'title' : 'Search Jobs',
            'desc' : "Post A Job To Tell Us About Your Project. We'll Quickly Match You With The Right Freelancers Find Place Best. Nor again is there anyone who loves.",
        },
        {
            'number' : '03.',
            'title' : 'Save & Apply Jobs',
            'desc' : "Post A Job To Tell Us About Your Project. We'll Quickly Match You With The Right Freelancers Find Place Best. Nor again is there anyone who loves.",
        }
    ]
    return {"needs": needs}


# explores data

def global_explores(request):
    explores = [
        {
            'img' : static('app/img/c-1.png'),
            'title' : 'California, USA',
            'jobs' : '307+ Jobs',
        },
        {
            'img' : static('app/img/c-2.png'),
            'title' : 'Denver City, USA',
            'jobs' : '102+ Jobs',
        },
        {
            'img' : static('app/img/c-3.png'),
            'title' : 'Washington, USA',
            'jobs' : '200+ Jobs',
        },
        {
            'img' : static('app/img/c-4.png'),
            'title' : 'Liverpool, UK',
            'jobs' : '150+ Jobs',
        }
    ]
    return {"explores": explores}


# candidates data

def global_candidates(request):
    candidates = [
        {
            'id' : 1,
            'img' : static('app/img/team-1.jpg'), 
            'title' : 'Kr. Shaurya Preet',
            'subtitle' : 'Sr. Web Designer',
            'number' : '70/H',
            'years' : '5 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 2,
            'img' : static('app/img/team-2.jpg'), 
            'title' : 'Leila T. Lindsey',
            'subtitle' : 'Magento Expert',
            'number' : '70/H',
            'years' : '5 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 3,
            'img' : static('app/img/team-3.jpg'), 
            'title' : 'Amie L. Brown',
            'subtitle' : 'WordPress Developer',
            'number' : '70/H',
            'years' : '5 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 4,
            'img' : static('app/img/team-4.jpg'), 
            'title' : 'Darrel T. Turner',
            'subtitle' : 'Jr. SEO Expert',
            'number' : '70/H',
            'years' : '5 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 5,
            'img' : static('app/img/team-5.jpg'), 
            'title' : 'Michael B. Arellano',
            'subtitle' : 'Front Designer',
            'number' : '70/H',
            'years' : '5 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 6,
            'img' : static('app/img/team-6.jpg'), 
            'title' : 'Kum K. Sellers',
            'subtitle' : 'PHP Developer',
            'number' : '70/H',
            'years' : '5 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 7,
            'img' : static('app/img/team-7.jpg'), 
            'title' : 'Debbie W. Wilson',
            'subtitle' : 'App Developer',
            'number' : '70/H',
            'years' : '5 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 8,
            'img' : static('app/img/team-8.jpg'), 
            'title' : 'Peggy J. Arnold',
            'subtitle' : 'Content Writer',
            'number' : '70/H',
            'years' : '5 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 9,
            'img' : static('app/img/team-9.jpg'), 
            'title' : 'Wanda D. Smith',
            'subtitle' : 'Sr. PHP Developer',
            'number' : '40/H',
            'years' : '2 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 10,
            'img' : static('app/img/team-10.jpg'), 
            'title' : 'Elaine W. Cook',
            'subtitle' : 'Sr. Team Leader',
            'number' : '65/H',
            'years' : '7 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 11,
            'img' : static('app/img/team-11.jpg'), 
            'title' : 'Raymond H. Cato',
            'subtitle' : 'UI/UX Designer',
            'number' : '50/H',
            'years' : '4 Years exp.',
            'btn' : 'Message',
            'btn1' : 'View Detail',
        },
        {
            'id' : 12,
            'img' : static('app/img/team-12.jpg'), 
            'title' : 'Ruth W. Guzman',
            'subtitle' : 'UI/UX Designer',
            'number' : '40/H',
            'years' : '3 Years exp.',
        },
        {
            'id' : 13,
            'img' : static('app/img/team-13.jpg'), 
            'title' : 'Shawnda J. Turner',
            'subtitle' : 'WordPress Developer',
            'number' : '35/H',
            'years' : '2 Years exp.',
        },
        {
            'id' : 14,
            'img' : static('app/img/team-14.jpg'), 
            'title' : 'Wlaine W. Cooke',
            'subtitle' : 'PHP Developer',
            'number' : '30/H',
            'years' : '2 Years exp.',
        },
        {
            'id' : 15,
            'img' : static('app/img/team-15.jpg'), 
            'title' : 'Jean H. Meyer',
            'subtitle' : 'Front-End Designer',
            'number' : '45/H',
            'years' : '5 Years exp.',
        }
    ]
    return {"candidates": candidates}


# jobs3 data

def global_jobs3(request):
    jobs3 = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'years' : '5 Years exp.', 
            'price' : '$370',
            'date' : '6 Sep 2025',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'years' : '3 Years exp.', 
            'price' : '$250',
            'date' : '10 Jan 2026',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'name' : 'Shopify', 
            'location' : 'London', 
            'time' : 'Enternship', 
            'years' : '2 Years exp.', 
            'price' : '$270',
            'date' : '5 Jan 2026',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'name' : 'Dreezoo', 
            'location' : 'New York', 
            'time' : 'Full Time', 
            'years' : '4 Years exp.', 
            'price' : '$350',
            'date' : '15 Jan 2026',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'name' : 'Snapchat', 
            'location' : 'California', 
            'time' : 'Part Time', 
            'years' : '4 Years exp.', 
            'price' : '$300',
            'date' : '26 Jan 2026',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'name' : 'Photoshop', 
            'location' : 'Canada', 
            'time' : 'Enternship', 
            'years' : '2 Years exp.', 
            'price' : '$290',
            'date' : '30 Jan 2026',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'name' : 'Firefox', 
            'location' : 'London', 
            'time' : 'Part Time', 
            'years' : '1 Years exp.', 
            'price' : '$180',
            'date' : '02 Feb 2026',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'name' : 'Airbnb', 
            'location' : 'London', 
            'time' : 'Freelance', 
            'years' : '2 Years exp.', 
            'price' : '$250',
            'date' : '10 Feb 2026',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'years' : '5 Years exp.', 
            'price' : '$370',
            'date' : '6 Sep 2025',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'years' : '3 Years exp.', 
            'price' : '$250',
            'date' : '10 Jan 2026',
        },
        {
            'id' : 11,
            'img' : static('app/img/l-11.png'), 
            'title' : 'Jr. Content Writer',
            'name' : 'Shopify', 
            'location' : 'London', 
            'time' : 'Enternship', 
            'years' : '2 Years exp.', 
            'price' : '$270',
            'date' : '5 Jan 2026',
        },
        {
            'id' : 12,
            'img' : static('app/img/l-12.png'), 
            'title' : 'Sr. Figma Designer',
            'name' : 'Dreezoo', 
            'location' : 'New York', 
            'time' : 'Full Time', 
            'years' : '4 Years exp.', 
            'price' : '$350',
            'date' : '15 Jan 2026',
        }
    ]
    return {"jobs3": jobs3}


# employers data

def global_employers(request):
    employers = [
        {
            'id' : 1,
            'img' : static('app/img/l-4.png'), 
            'name' : 'Software & Consultancy', 
            'title' : 'Swap Technology',
            'location' : 'California, USA', 
            'open' : '06 Open position', 
        },
        {
            'id' : 2,
            'img' : static('app/img/l-5.png'), 
            'name' : 'Photo Edditing Tools', 
            'title' : 'Photoshop',
            'location' : 'New York, USA', 
            'open' : '16 Open position', 
        },
        {
            'id' : 3,
            'img' : static('app/img/l-6.png'), 
            'name' : 'Web Browser & Tech', 
            'title' : 'Firefox',
            'location' : 'Denver, USA', 
            'open' : '03 Open position', 
        },
        {
            'id' : 4,
            'img' : static('app/img/l-7.png'), 
            'name' : 'Business Directory', 
            'title' : 'Airbnb',
            'location' : 'London, UK', 
            'open' : '08 Open position', 
        },
        {
            'id' : 5,
            'img' : static('app/img/l-8.png'), 
            'name' : 'Message & Video Reelas', 
            'title' : 'Snapchat',
            'location' : 'London, UK', 
            'open' : '07 Open position', 
        },
        {
            'id' : 6,
            'img' : static('app/img/l-9.png'), 
            'name' : 'Portfolio Showcase', 
            'title' : 'Dribbble Inc',
            'location' : 'New York, USA', 
            'open' : '05 Open position', 
        },
        {
            'id' : 7,
            'img' : static('app/img/l-10.png'), 
            'name' : 'Chat & Video Calling', 
            'title' : 'Skype',
            'location' : 'Canada, USA', 
            'open' : '10 Open position', 
        },
        {
            'id' : 8,
            'img' : static('app/img/l-11.png'), 
            'name' : 'Software & Consultancy', 
            'title' : 'Google Inc',
            'location' : 'London, UK', 
            'open' : '06 Open position', 
        },
        {
            'id' : 9,
            'img' : static('app/img/l-2.png'), 
            'name' : 'Photo Showcase & Tools', 
            'title' : 'Pinterest - Punjab',
            'location' : 'Austrailia', 
            'open' : '03 Openings', 
            'est' : 'Est: 2003', 
        },
        {
            'id' : 10,
            'img' : static('app/img/l-3.png'), 
            'name' : 'Web & Applications', 
            'title' : 'Shopify - Delhi',
            'location' : 'Canada, USA', 
            'open' : '05 Openings', 
            'est' : 'Est: 1980', 
        }
    ]
    return {"employers": employers}


# jobs4 data

def global_jobs4(request):
    jobs4 = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'app' : 'Tripadvisor',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'London',
            'time' : 'Full Time',
            'ago' : '1 Hours ago',
            'price' : '$80K - 90K', 
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'app' : 'Pinterest',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'USA',
            'time' : 'Part Time',
            'ago' : '10 Hours ago',
            'price' : '$90K - 100K',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'app' : 'Shopify',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'Canada',
            'time' : 'Enternship',
            'ago' : '1 Days ago',
            'price' : '$75K - 90K',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'app' : 'Dreezoo',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'Canada',
            'time' : 'Full Time',
            'ago' : '1 Days ago',
            'price' : '$65K - 80K',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'app' : 'Photoshop',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'New York',
            'time' : 'Part Time',
            'ago' : '2 Days ago',
            'price' : '$95K - 120K',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'app' : 'Firefox',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'Denver',
            'time' : 'Freelance',
            'ago' : '2 Days ago',
            'price' : '$90K - 110K',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'app' : 'Airbnb',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'London',
            'time' : 'Full Time',
            'ago' : '2 Days ago',
            'price' : '$60K - 80K',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'app' : 'Snapchat',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'Canada',
            'time' : 'Part Time',
            'ago' : '3 Days ago',
            'price' : '$80K - 95K',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'app' : 'Tripadvisor',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'London',
            'time' : 'Full Time',
            'ago' : '1 Hours ago',
            'price' : '$80K - 90K', 
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'app' : 'Pinterest',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'USA',
            'time' : 'Part Time',
            'ago' : '10 Hours ago',
            'price' : '$90K - 100K',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 11,
            'img' : static('app/img/l-11.png'), 
            'title' : 'Jr. Content Writer',
            'app' : 'Shopify',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'Canada',
            'time' : 'Enternship',
            'ago' : '1 Days ago',
            'price' : '$75K - 90K',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 12,
            'img' : static('app/img/l-12.png'), 
            'title' : 'Sr. Figma Designer',
            'app' : 'Dreezoo',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'location' : 'Canada',
            'time' : 'Full Time',
            'ago' : '1 Days ago',
            'price' : '$65K - 80K',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        }
    ]
    return {"jobs4": jobs4}


# blogs data

def global_blogs(request):
    blogs = [
        {
            'id' : 1,
            'img' : static('app/img/blog-1.jpg'), 
            'title' : 'How To Work with jobstock Agency',
            'desc' : 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat',
            'date' : '10 Jul 2026',
        },
        {
            'id' : 2,
            'img' : static('app/img/blog-2.jpg'), 
            'title' : 'Auctor sit elementum habitant vel tempor varius.',
            'desc' : 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat',
            'date' : '17 Jan 2026',
        },
        {
            'id' : 3,
            'img' : static('app/img/blog-3.jpg'), 
            'title' : 'Consectetur purus habitasse ut diam habitant varius.',
            'desc' : 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat',
            'date' : '26 Feb 2026',
        },
        {
            'id' : 4,
            'img' : static('app/img/blog-7.jpg'), 
            'title' : 'Smartest Applications for Business',
            'desc' : 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat',
            'date' : '19 Dec 2026',
        },
        {
            'id' : 5,
            'img' : static('app/img/blog-4.jpg'), 
            'title' : 'Stop Worrying About Deadlines! We Got You Covered',
            'desc' : 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat',
            'date' : '10 Aug 2026',
        },
        {
            'id' : 6,
            'img' : static('app/img/blog-5.jpg'), 
            'title' : 'Change Your Strategy: Find a Business Consultant',
            'desc' : 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat',
            'date' : '16 Jul 2026',
        },
        {
            'id' : 7,
            'img' : static('app/img/blog-6.jpg'), 
            'title' : 'Everything About Financial Modeling',
            'desc' : 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat',
            'date' : '07 May 2026',
        },
        {
            'id' : 8,
            'img' : static('app/img/blog-7.jpg'), 
            'title' : 'On the other hand we provide denounce',
            'desc' : 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat',
            'date' : '19 Dec 2026',
        }
    ]
    return {"blogs": blogs}


# categories2 data

def global_categories2(request):
    categories2 = [
        {
            'icon' : 'fa-solid fa-file-invoice',
            'title' : 'Accounting & Finance',
            'desc' : 'You can view all popular jobs according your future careers.',
            'jobs' : '122 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-caravan',
            'title' : 'Automotive Jobs',
            'desc' : 'You can view all popular jobs according your future careers.',
            'jobs' : '78 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-person-chalkboard',
            'title' : 'Business & Tech',
            'desc' : 'You can view all popular jobs according your future careers.',
            'jobs' : '25 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-user-graduate',
            'title' : 'Education Training',
            'desc' : 'You can view all popular jobs according your future careers.',
            'jobs' : '212 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-briefcase-medical',
            'title' : 'Healthcare',
            'desc' : 'You can view all popular jobs according your future careers.',
            'jobs' : '90 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-burger',
            'title' : 'Restaurant & Food',
            'desc' : 'You can view all popular jobs according your future careers.',
            'jobs' : '65 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-jet-fighter',
            'title' : 'Transportation',
            'desc' : 'You can view all popular jobs according your future careers.',
            'jobs' : '160 Active Jobs',
        },
        {
            'icon' : 'fa-solid fa-mobile-screen-button',
            'title' : 'Telecommunications',
            'desc' : 'You can view all popular jobs according your future careers.',
            'jobs' : '80 Active Jobs',
        }
    ]
    return {"categories2": categories2}


# ctrs2 data

def global_ctrs2(request):
    ctrs2 = [
        {
            'title' : 'Success in finding jobs on JobStock Platform',
            'number' : '97',
            'symbol' : '%',
        },
        {
            'title' : 'Potential increase traffice rather than JobStock website.',
            'number' : '68',
            'symbol' : 'X',
        },
        {
            'title' : 'Thousands of companies work with us with partnership',
            'number' : '25',
            'symbol' : 'K',
        },
        {
            'title' : 'Happy customers in all over world with our services',
            'number' : '25',
            'symbol' : 'K',
        }
    ]
    return {"ctrs2": ctrs2}


# clients data

def global_clients(request):
    clients = [
        {
            'name' : 'Chad B. Werner',
            'title' : 'Web Designer',
            'desc' : 'The wise man therefore always circumstances and owing to the claims of duty or the obligations holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.',
            'class' : 'show active',
            'id' : 'pills-track-1',
            'labelledby' : 'pills-track-1-tab',
        },
        {
            'name' : 'Melvin D. Fowler',
            'title' : 'Team Manager',
            'desc' : 'The wise man therefore always circumstances and owing to the claims of duty or the obligations holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.',
            'class' : '',
            'id' : 'pills-track-2',
            'labelledby' : 'pills-track-2-tab',
        },
        {
            'name' : 'Chad B. Werner',
            'title' : 'Web Designer',
            'desc' : 'The wise man therefore always circumstances and owing to the claims of duty or the obligations holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.',
            'class' : '',
            'id' : 'pills-track-3',
            'labelledby' : 'pills-track-3-tab',
        },
        {
            'name' : 'Sylvester B. Blevins',
            'title' : 'WordPress Developer',
            'desc' : 'The wise man therefore always circumstances and owing to the claims of duty or the obligations holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.',
            'class' : '',
            'id' : 'pills-track-4',
            'labelledby' : 'pills-track-4-tab',
        },
        {
            'name' : 'Jacob R. Haynes',
            'title' : 'Sr. PHP Developer',
            'desc' : 'The wise man therefore always circumstances and owing to the claims of duty or the obligations holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.',
            'class' : '',
            'id' : 'pills-track-5',
            'labelledby' : 'pills-track-5-tab',
        }
    ]
    return {"clients": clients}


# tablists data

def global_tablists(request):
    tablists = [
        {
            'img' : static('app/img/team-1.jpg'),
            'class' : 'active',
            'id' : 'pills-track-1-tab',
            'target' : '#pills-track-1',
            'controls' : 'pills-track-1',
            'selected' : 'true',
        },
        {
            'img' : static('app/img/team-2.jpg'),
            'class' : '',
            'id' : 'pills-track-2-tab',
            'target' : '#pills-track-2',
            'controls' : 'pills-track-2',
            'selected' : 'false',
        },
        {
            'img' : static('app/img/team-3.jpg'),
            'class' : '',
            'id' : 'pills-track-3-tab',
            'target' : '#pills-track-3',
            'controls' : 'pills-track-3',
            'selected' : 'false',
        },
        {
            'img' : static('app/img/team-5.jpg'),
            'class' : '',
            'id' : 'pills-track-4-tab',
            'target' : '#pills-track-4',
            'controls' : 'pills-track-4',
            'selected' : 'false',
        },
        {
            'img' : static('app/img/team-6.jpg'),
            'class' : '',
            'id' : 'pills-track-5-tab',
            'target' : '#pills-track-5',
            'controls' : 'pills-track-5',
            'selected' : 'false',
        }
    ]
    return {"tablists": tablists}


# jobs5 data

def global_jobs5(request):
    jobs5 = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '6 Open', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$6K - $10K', 
            'open' : '4 Open', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '3 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$4.2K - $6K', 
            'open' : '2 Open', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$4K - $5.5K', 
            'open' : '5 Open', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$2K - $4K', 
            'open' : '4 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $6K', 
            'open' : '3 Open', 
            'tag' : 'FullTime',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$3.2K - $5K', 
            'open' : '5 Open', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$85K - 90K', 
            'open' : '1 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$70K - 95K', 
            'open' : '4 Open', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 11,
            'img' : static('app/img/l-11.png'), 
            'title' : 'Jr. Content Writer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$4K - $5.5K', 
            'open' : '2 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 12,
            'img' : static('app/img/l-12.png'), 
            'title' : 'Sr. Figma Designer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$6K - $8K', 
            'open' : '3 Open', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '6 Open', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$6K - $10K', 
            'open' : '4 Open', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '3 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        }
    ]
    return {"jobs5": jobs5}


# jobs6 data

def global_jobs6(request):
    jobs6 = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'app' : 'Tripadvisor',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'year' : '1-2 Year',
            'time' : 'Full Time',
            'location' : 'London',
            'price' : '$370',
            'date' : '6 Sep 2025',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'app' : 'Pinterest',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'year' : '1-2 Year',
            'time' : 'Full Time',
            'location' : 'London',
            'price' : '$370',
            'date' : '6 Sep 2025',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'app' : 'Shopify',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'year' : '1-2 Year',
            'time' : 'Full Time',
            'location' : 'London',
            'price' : '$370',
            'date' : '6 Sep 2025',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'app' : 'Dreezoo',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'year' : '1-2 Year',
            'time' : 'Full Time',
            'location' : 'London',
            'price' : '$370',
            'date' : '6 Sep 2025',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'app' : 'Photoshop',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'year' : '1-2 Year',
            'time' : 'Full Time',
            'location' : 'London',
            'price' : '$370',
            'date' : '6 Sep 2025',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'app' : 'Firefox',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'year' : '1-2 Year',
            'time' : 'Full Time',
            'location' : 'London',
            'price' : '$370',
            'date' : '6 Sep 2025',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'app' : 'Airbnb',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'year' : '1-2 Year',
            'time' : 'Full Time',
            'location' : 'London',
            'price' : '$370',
            'date' : '6 Sep 2025',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'app' : 'Snapchat',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'year' : '1-2 Year',
            'time' : 'Full Time',
            'location' : 'London',
            'price' : '$370',
            'date' : '6 Sep 2025',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'app' : 'Tripadvisor',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'year' : '1-2 Year',
            'time' : 'Full Time',
            'location' : 'London',
            'price' : '$370',
            'date' : '6 Sep 2025',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'app' : 'Pinterest',
            'desc' : 'Consistently create well-designed, tested code using best practices for website development, including mobile...',
            'year' : '1-2 Year',
            'time' : 'Full Time',
            'location' : 'London',
            'price' : '$370',
            'date' : '6 Sep 2025',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        }
    ]
    return {"jobs6": jobs6}


# jobs7 data

def global_jobs7(request):
    jobs7 = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '6 Open', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$6K - $10K', 
            'open' : '4 Open', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '3 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$4.2K - $6K', 
            'open' : '2 Open', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$4K - $5.5K', 
            'open' : '5 Open', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$2K - $4K', 
            'open' : '4 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '6 Open', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $6K', 
            'open' : '3 Open', 
            'tag' : 'FullTime',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$3.2K - $5K', 
            'open' : '5 Open', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$85K - 90K', 
            'open' : '1 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$70K - 95K', 
            'open' : '4 Open', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 11,
            'img' : static('app/img/l-11.png'), 
            'title' : 'Jr. Content Writer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$4K - $5.5K', 
            'open' : '2 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 12,
            'img' : static('app/img/l-12.png'), 
            'title' : 'Sr. Figma Designer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$6K - $8K', 
            'open' : '3 Open', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '6 Open', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$6K - $10K', 
            'open' : '4 Open', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $8K', 
            'open' : '3 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$2K - $4K', 
            'open' : '4 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$5K - $6K', 
            'open' : '3 Open', 
            'tag' : 'FullTime',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$3.2K - $5K', 
            'open' : '5 Open', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'desc' : 'CSS3, HTML5, Javascript, Bootstrap, Jquery',
            'price' : '$85K - 90K', 
            'open' : '1 Open', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        }
    ]
    return {"jobs7": jobs7}


# jobs8 data

def global_jobs8(request):
    jobs8 = [
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'app' : 'Shopify',
            'location' : 'London, UK',
            'price' : '$80K - 110K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'app' : 'Deezroo',
            'location' : 'Canada, USA',
            'price' : '$50K - 70K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'app' : 'Deezroo',
            'location' : 'Canada, USA',
            'price' : '$50K - 70K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'app' : 'Shopify',
            'location' : 'London, UK',
            'price' : '$80K - 110K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'app' : 'Dribbble',
            'location' : 'New York, USA',
            'price' : '$85K - 90K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'app' : 'Skype',
            'location' : 'Denver, USA',
            'price' : '$70K - 95K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'app' : 'Photoshop',
            'location' : 'Denver, USA',
            'price' : '$80K - 90K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'app' : 'Firefox',
            'location' : 'California, USA',
            'price' : '$90K - 100K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Part Time',
            'style' : 'part-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'app' : 'Air BNB',
            'location' : 'Canada, USA',
            'price' : '$80K - 110K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'app' : 'Snapchat',
            'location' : 'London, UK',
            'price' : '$60K - 90K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : False,
            'name' : 'Urgent',
            'class' : 'urgent',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'app' : 'Dribbble',
            'location' : 'New York, USA',
            'price' : '$85K - 90K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'app' : 'Skype',
            'location' : 'Denver, USA',
            'price' : '$70K - 95K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'app' : 'Deezroo',
            'location' : 'Canada, USA',
            'price' : '$50K - 70K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Enternship',
            'style' : 'enternship',
            'tag1' : True,
            'name' : '',
            'class' : '',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'app' : 'Shopify',
            'location' : 'London, UK',
            'price' : '$80K - 110K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'app' : 'Dribbble',
            'location' : 'New York, USA',
            'price' : '$85K - 90K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Freelancer',
            'style' : 'freelanc',
            'tag1' : False,
            'name' : 'Featured',
            'class' : 'featured-text',
        },
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'app' : 'Skype',
            'location' : 'Denver, USA',
            'price' : '$70K - 95K', 
            'btn' : 'Quick Apply', 
            'tag' : 'Full Time',
            'style' : 'full-time',
            'tag1' : True,
            'name' : '',
            'class' : '',
        }
    ]
    return {"jobs8": jobs8}


# jobs9 data

def global_jobs9(request):
    jobs9 = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'years' : '5 Years exp.', 
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'years' : '3 Years exp.', 
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'name' : 'Shopify', 
            'location' : 'London', 
            'time' : 'Enternship', 
            'years' : '2 Years exp.', 
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'name' : 'Dreezoo', 
            'location' : 'New York', 
            'time' : 'Full Time', 
            'years' : '4 Years exp.', 
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'name' : 'Snapchat', 
            'location' : 'California', 
            'time' : 'Part Time', 
            'years' : '4 Years exp.', 
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'name' : 'Photoshop', 
            'location' : 'Canada', 
            'time' : 'Enternship', 
            'years' : '2 Years exp.', 
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'name' : 'Firefox', 
            'location' : 'London', 
            'time' : 'Part Time', 
            'years' : '1 Years exp.', 
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'name' : 'Airbnb', 
            'location' : 'London', 
            'time' : 'Freelance', 
            'years' : '2 Years exp.', 
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'years' : '5 Years exp.', 
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'years' : '3 Years exp.', 
        }
    ]
    return {"jobs9": jobs9}


# jobs10 data

def global_jobs10(request):
    jobs10 = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'date' : '06 Sep 2025', 
            'price' : '$85K - 95K',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'price' : '$85K - 95K',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'name' : 'Shopify', 
            'location' : 'London', 
            'time' : 'Enternship', 
            'date' : '06 Sep 2025', 
            'price' : '$85K - 95K',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'name' : 'Dreezoo', 
            'location' : 'New York', 
            'time' : 'Full Time', 
            'date' : '06 Sep 2025', 
            'price' : '$85K - 95K',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'name' : 'Snapchat', 
            'location' : 'California', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'price' : '$85K - 95K',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'name' : 'Photoshop', 
            'location' : 'Canada', 
            'time' : 'Enternship', 
            'date' : '06 Sep 2025', 
            'price' : '$85K - 95K',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'name' : 'Firefox', 
            'location' : 'London', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'price' : '$85K - 95K',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'name' : 'Airbnb', 
            'location' : 'London', 
            'time' : 'Freelance', 
            'date' : '06 Sep 2025', 
            'price' : '$85K - 95K',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'date' : '06 Sep 2025', 
            'price' : '$85K - 95K',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'price' : '$85K - 95K',
        }
    ]
    return {"jobs10": jobs10}


# informations data

def global_informations(request):
    informations = [
        {
            'icon' : 'fa-solid fa-envelope-open-text', 
            'title' : 'shreethemes@gmail.com',
            'name' : 'Mail Address',
        },
        {
            'icon' : 'fa-solid fa-phone-volume', 
            'title' : '855 606 8472',
            'name' : 'Phone No.',
        },
        {
            'icon' : 'fa-regular fa-user', 
            'title' : 'Male',
            'name' : 'Gender',
        },
        {
            'icon' : 'fa-solid fa-cake-candles', 
            'title' : '07 Apr 1992',
            'name' : 'Age',
        },
        {
            'icon' : 'fa-solid fa-wallet', 
            'title' : '$750/month',
            'name' : 'Offerd Sallary',
        },
        {
            'icon' : 'fa-solid fa-briefcase', 
            'title' : '5 Years',
            'name' : 'Experience',
        },
        {
            'icon' : 'fa-solid fa-user-graduate', 
            'title' : 'Master Degree',
            'name' : 'Qualification',
        },
        {
            'icon' : 'fa-solid fa-layer-group', 
            'title' : 'Fulltime, Remote, Freelance',
            'name' : 'Work Type',
        }
    ]
    return {"informations": informations}


# jobs11 data

def global_jobs11(request):
    jobs11 = [
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'name' : 'Firefox', 
            'location' : 'London', 
            'time' : 'Part Time', 
            'years' : '$400', 
            'ago' : '05 Days ago',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'name' : 'Airbnb', 
            'location' : 'London', 
            'time' : 'Freelance', 
            'years' : '$320', 
            'ago' : '05 Days ago',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'years' : '$400', 
            'ago' : '07 Days ago',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'years' : '$350', 
            'ago' : '08 Days ago',
        },
        {
            'id' : 11,
            'img' : static('app/img/l-11.png'), 
            'title' : 'Jr. Content Writer',
            'name' : 'Shopify', 
            'location' : 'London', 
            'time' : 'Enternship', 
            'years' : '$290', 
            'ago' : '10 Days ago',
        },
        {
            'id' : 12,
            'img' : static('app/img/l-12.png'), 
            'title' : 'Sr. Figma Designer',
            'name' : 'Dreezoo', 
            'location' : 'New York', 
            'time' : 'Full Time', 
            'years' : '$250', 
            'ago' : '15 Days ago',
        },
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'years' : '$370', 
            'ago' : '07 Days ago',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'years' : '$370', 
            'ago' : '10 min ago',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'name' : 'Shopify', 
            'location' : 'London', 
            'time' : 'Enternship', 
            'years' : '$300', 
            'ago' : '2 Hours ago',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'name' : 'Dreezoo', 
            'location' : 'New York', 
            'time' : 'Full Time', 
            'years' : '$290', 
            'ago' : '5 Hours ago',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'name' : 'Snapchat', 
            'location' : 'California', 
            'time' : 'Part Time', 
            'years' : '$310', 
            'ago' : '10 Hours ago',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'name' : 'Photoshop', 
            'location' : 'Canada', 
            'time' : 'Enternship', 
            'years' : '$450', 
            'ago' : '02 Days ago',
        }
    ]
    return {"jobs11": jobs11}


# jobs12 data

def global_jobs12(request):
    jobs12 = [
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'name' : 'Snapchat', 
            'location' : 'California', 
            'time' : 'Part Time', 
            'years' : '$310', 
            'ago' : '10 Hours ago',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'name' : 'Photoshop', 
            'location' : 'Canada', 
            'time' : 'Enternship', 
            'years' : '$450', 
            'ago' : '02 Days ago',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'name' : 'Firefox', 
            'location' : 'London', 
            'time' : 'Part Time', 
            'years' : '$400', 
            'ago' : '05 Days ago',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'name' : 'Airbnb', 
            'location' : 'London', 
            'time' : 'Freelance', 
            'years' : '$320', 
            'ago' : '05 Days ago',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'years' : '$400', 
            'ago' : '07 Days ago',
        },
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'years' : '$370', 
            'ago' : '07 Days ago',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'years' : '$370', 
            'ago' : '10 min ago',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'name' : 'Shopify', 
            'location' : 'London', 
            'time' : 'Enternship', 
            'years' : '$300', 
            'ago' : '2 Hours ago',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'name' : 'Dreezoo', 
            'location' : 'New York', 
            'time' : 'Full Time', 
            'years' : '$290', 
            'ago' : '5 Hours ago',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'years' : '$350', 
            'ago' : '08 Days ago',
        },
        {
            'id' : 11,
            'img' : static('app/img/l-11.png'), 
            'title' : 'Jr. Content Writer',
            'name' : 'Shopify', 
            'location' : 'London', 
            'time' : 'Enternship', 
            'years' : '$290', 
            'ago' : '10 Days ago',
        },
        {
            'id' : 12,
            'img' : static('app/img/l-12.png'), 
            'title' : 'Sr. Figma Designer',
            'name' : 'Dreezoo', 
            'location' : 'New York', 
            'time' : 'Full Time', 
            'years' : '$250', 
            'ago' : '15 Days ago',
        }
    ]
    return {"jobs12": jobs12}


# ctrs3 data

def global_ctrs3(request):
    ctrs3 = [
        {
            'icon' : 'fa-solid fa-business-time', 
            'class' : 'success',
            'title' : 'Applied jobs',
            'number' : '523',
        },
        {
            'icon' : 'fa-solid fa-bookmark', 
            'class' : 'warning',
            'title' : 'Saved Jobs',
            'number' : '523',
        },
        {
            'icon' : 'fa-solid fa-eye', 
            'class' : 'danger',
            'title' : 'Viewed Jobs',
            'number' : '523',
        },
        {
            'icon' : 'fa-sharp fa-solid fa-comments', 
            'class' : 'info',
            'title' : 'Total Review',
            'number' : '523',
        }
    ]
    return {"ctrs3": ctrs3}


# jobs13 data

def global_jobs13(request):
    jobs13 = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'date' : '06 Sep 2025', 
            'apply' : 'Apply 02 Jun 2025',
            'btn' : 'Approved',
            'class' : 'success',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'apply' : 'Apply 02 Jun 2025',
            'btn' : 'Pending',
            'class' : 'warning',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'name' : 'Shopify', 
            'location' : 'London', 
            'time' : 'Enternship', 
            'date' : '06 Sep 2025', 
            'apply' : 'Apply 02 Jun 2025',
            'btn' : 'Approved',
            'class' : 'success',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'name' : 'Dreezoo', 
            'location' : 'New York', 
            'time' : 'Full Time', 
            'date' : '06 Sep 2025', 
            'apply' : 'Apply 02 Jun 2025',
            'btn' : 'Pending',
            'class' : 'warning',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'name' : 'Snapchat', 
            'location' : 'California', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'apply' : 'Apply 02 Jun 2025',
            'btn' : 'Approved',
            'class' : 'success',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'name' : 'Photoshop', 
            'location' : 'Canada', 
            'time' : 'Enternship', 
            'date' : '06 Sep 2025', 
            'apply' : 'Apply 02 Jun 2025',
            'btn' : 'Approved',
            'class' : 'success',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'name' : 'Firefox', 
            'location' : 'London', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'apply' : 'Apply 02 Jun 2025',
            'btn' : 'Pending',
            'class' : 'warning',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'name' : 'Airbnb', 
            'location' : 'London', 
            'time' : 'Freelance', 
            'date' : '06 Sep 2025', 
            'apply' : 'Apply 02 Jun 2025',
            'btn' : 'Approved',
            'class' : 'success',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'date' : '06 Sep 2025', 
            'apply' : 'Apply 02 Jun 2025',
            'btn' : 'Pending',
            'class' : 'warning',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'apply' : 'Apply 02 Jun 2025',
            'btn' : 'Pending',
            'class' : 'warning',
        }
    ]
    return {"jobs13": jobs13}


# jobs14 data

def global_jobs14(request):
    jobs14 = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'date' : '06 Sep 2025', 
            'apply' : '27 Applied',
            'btn' : 'Active',
            'class' : 'success',
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'apply' : '27 Applied',
            'btn' : 'Expired',
            'class' : 'danger',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'name' : 'Shopify', 
            'location' : 'London', 
            'time' : 'Enternship', 
            'date' : '06 Sep 2025', 
            'apply' : '27 Applied',
            'btn' : 'Active',
            'class' : 'success',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'name' : 'Dreezoo', 
            'location' : 'New York', 
            'time' : 'Full Time', 
            'date' : '06 Sep 2025', 
            'apply' : '27 Applied',
            'btn' : 'Expired',
            'class' : 'danger',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'name' : 'Snapchat', 
            'location' : 'California', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'apply' : '27 Applied',
            'btn' : 'Active',
            'class' : 'success',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'name' : 'Photoshop', 
            'location' : 'Canada', 
            'time' : 'Enternship', 
            'date' : '06 Sep 2025', 
            'apply' : '27 Applied',
            'btn' : 'Active',
            'class' : 'success',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'name' : 'Firefox', 
            'location' : 'London', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'apply' : '27 Applied',
            'btn' : 'Expired',
            'class' : 'danger',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'name' : 'Airbnb', 
            'location' : 'London', 
            'time' : 'Freelance', 
            'date' : '06 Sep 2025', 
            'apply' : '27 Applied',
            'btn' : 'Active',
            'class' : 'success',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'name' : 'Tripadvisor', 
            'location' : 'London', 
            'time' : 'Full Time', 
            'date' : '06 Sep 2025', 
            'apply' : '27 Applied',
            'btn' : 'Expired',
            'class' : 'danger',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'name' : 'Pinterest', 
            'location' : 'Canada', 
            'time' : 'Part Time', 
            'date' : '06 Sep 2025', 
            'apply' : '27 Applied',
            'btn' : 'Expired',
            'class' : 'danger',
        }
    ]
    return {"jobs14": jobs14}


# employers2 data

def global_employers2(request):
    employers2 = [
        {
            'id' : 1,
            'img' : static('app/img/l-4.png'), 
            'name' : 'Software & Consultancy', 
            'title' : 'Swap Technology',
            'location' : 'California, USA', 
            'open' : '06 Open position', 
        },
        {
            'id' : 2,
            'img' : static('app/img/l-5.png'), 
            'name' : 'Photo Edditing Tools', 
            'title' : 'Photoshop',
            'location' : 'New York, USA', 
            'open' : '16 Open position', 
        },
        {
            'id' : 3,
            'img' : static('app/img/l-6.png'), 
            'name' : 'Web Browser & Tech', 
            'title' : 'Firefox',
            'location' : 'Denver, USA', 
            'open' : '03 Open position', 
        },
        {
            'id' : 4,
            'img' : static('app/img/l-7.png'), 
            'name' : 'Business Directory', 
            'title' : 'Airbnb',
            'location' : 'London, UK', 
            'open' : '08 Open position', 
        },
        {
            'id' : 5,
            'img' : static('app/img/l-8.png'), 
            'name' : 'Message & Video Reelas', 
            'title' : 'Snapchat',
            'location' : 'London, UK', 
            'open' : '07 Open position', 
        },
        {
            'id' : 6,
            'img' : static('app/img/l-9.png'), 
            'name' : 'Portfolio Showcase', 
            'title' : 'Dribbble Inc',
            'location' : 'New York, USA', 
            'open' : '05 Open position', 
        },
        {
            'id' : 7,
            'img' : static('app/img/l-10.png'), 
            'name' : 'Chat & Video Calling', 
            'title' : 'Skype',
            'location' : 'Canada, USA', 
            'open' : '10 Open position', 
        },
        {
            'id' : 8,
            'img' : static('app/img/l-11.png'), 
            'name' : 'Software & Consultancy', 
            'title' : 'Google Inc',
            'location' : 'London, UK', 
            'open' : '06 Open position', 
        },
        {
            'id' : 1,
            'img' : static('app/img/l-4.png'), 
            'name' : 'Software & Consultancy', 
            'title' : 'Swap Technology',
            'location' : 'California, USA', 
            'open' : '06 Open position', 
        },
        {
            'id' : 2,
            'img' : static('app/img/l-5.png'), 
            'name' : 'Photo Edditing Tools', 
            'title' : 'Photoshop',
            'location' : 'New York, USA', 
            'open' : '16 Open position', 
        },
        {
            'id' : 3,
            'img' : static('app/img/l-6.png'), 
            'name' : 'Web Browser & Tech', 
            'title' : 'Firefox',
            'location' : 'Denver, USA', 
            'open' : '03 Open position', 
        },
        {
            'id' : 4,
            'img' : static('app/img/l-7.png'), 
            'name' : 'Business Directory', 
            'title' : 'Airbnb',
            'location' : 'London, UK', 
            'open' : '08 Open position', 
        }
    ]
    return {"employers2": employers2}


# awards data

def global_awards(request):
    awards = [
        {
            'img' : static('app/img/award-1.png'), 
            'title' : 'FIFFA Award',
            'year' : 'May 2025',
        },
        {
            'img' : static('app/img/award-2.png'), 
            'title' : 'COMPRA Award',
            'year' : 'Dec 2024',
        },
        {
            'img' : static('app/img/award-4.png'), 
            'title' : 'ICCPR Award',
            'year' : 'Apr 2023',
        },
        {
            'img' : static('app/img/award-3.png'), 
            'title' : 'XICAGO Award',
            'year' : 'July 2022',
        }
    ]
    return {"awards": awards}


# views data

def global_views(request):
    views = [
        {
            'icon' : 'fa-solid fa-envelope-circle-check text-main', 
            'title' : 'Email Address',
            'name' : 'shreethemes@gmail.com',
        },
        {
            'icon' : 'fa-solid fa-phone-volume text-main', 
            'title' : 'Contact No.',
            'name' : '9450 542 6325',
        },
        {
            'icon' : 'fa-solid fa-layer-group text-main', 
            'title' : 'Category',
            'name' : 'Applications',
        },
        {
            'icon' : 'fa-solid fa-user-group text-main', 
            'title' : 'Company Size',
            'name' : '1000-1500',
        },
        {
            'icon' : 'fa-solid fa-map-location-dot text-main', 
            'title' : 'Location',
            'name' : 'California, USA',
        },
        {
            'icon' : 'fa-solid fa-building-circle-check text-main', 
            'title' : 'Established',
            'name' : 'Oct 2010',
        }
    ]
    return {"views": views}


# ctrs4 data

def global_ctrs4(request):
    ctrs4 = [
        {
            'icon' : 'fa-solid fa-business-time', 
            'class' : 'success', 
            'number' : '760',
            'title' : 'Posted jobs',
        },
        {
            'icon' : 'fa-solid fa-bookmark', 
            'class' : 'warning', 
            'number' : '12560',
            'title' : 'Saved Candidates',
        },
        {
            'icon' : 'fa-solid fa-user-clock', 
            'class' : 'danger', 
            'number' : '672',
            'title' : 'Applicants',
        },
        {
            'icon' : 'fa-sharp fa-solid fa-comments', 
            'class' : 'info', 
            'number' : '215',
            'title' : 'Total Review',
        }
    ]
    return {"ctrs4": ctrs4}


# posteds data

def global_posteds(request):
    posteds = [
        {
            'id' : 1,
            'img' : static('app/img/l-1.png'), 
            'title' : 'Jr. PHP Developer',
            'name' : 'Tripadvisor', 
            'applicants' : '244 Applicants', 
            'class' : 'green', 
            'posted' : '17 Apr 2025', 
            'expired' : '12 Jun 2026', 
        },
        {
            'id' : 2,
            'img' : static('app/img/l-2.png'), 
            'title' : 'Exp. Project manager',
            'name' : 'Pinterest', 
            'applicants' : '110 Applicants', 
            'class' : 'green', 
            'posted' : '17 Apr 2025', 
            'expired' : '12 Jun 2026',
        },
        {
            'id' : 3,
            'img' : static('app/img/l-3.png'), 
            'title' : 'Sr. WordPress Developer',
            'name' : 'Shopify', 
            'applicants' : '320 Applicants', 
            'class' : 'green', 
            'posted' : '17 Apr 2025', 
            'expired' : '12 Jun 2026',
        },
        {
            'id' : 4,
            'img' : static('app/img/l-4.png'), 
            'title' : 'Jr. Laravel Developer',
            'name' : 'Dreezoo', 
            'applicants' : '170 Applicants', 
            'class' : 'green', 
            'posted' : '17 Apr 2025', 
            'expired' : '12 Jun 2026',
        },
        {
            'id' : 5,
            'img' : static('app/img/l-5.png'), 
            'title' : 'Sr. UI/UX Designer',
            'name' : 'Snapchat', 
            'applicants' : '190 Applicants', 
            'class' : 'green', 
            'posted' : '17 Apr 2025', 
            'expired' : '12 Jun 2026',
        },
        {
            'id' : 6,
            'img' : static('app/img/l-6.png'), 
            'title' : 'Java & Python Developer',
            'name' : 'Photoshop', 
            'applicants' : 'Expired', 
            'class' : 'red', 
            'posted' : '17 Apr 2025', 
            'expired' : '12 Jun 2026',
        },
        {
            'id' : 7,
            'img' : static('app/img/l-7.png'), 
            'title' : 'Sr. CodeIgniter Developer',
            'name' : 'Firefox', 
            'applicants' : '205 Applicants', 
            'class' : 'green', 
            'posted' : '17 Apr 2025', 
            'expired' : '12 Jun 2026',
        },
        {
            'id' : 8,
            'img' : static('app/img/l-8.png'), 
            'title' : 'Sr. Magento Developer',
            'name' : 'Airbnb', 
            'applicants' : '320 Applicants', 
            'class' : 'green', 
            'posted' : '17 Apr 2025', 
            'expired' : '12 Jun 2026',
        },
        {
            'id' : 9,
            'img' : static('app/img/l-9.png'), 
            'title' : 'Technical Content Writer',
            'name' : 'Tripadvisor', 
            'applicants' : 'Expired', 
            'class' : 'red', 
            'posted' : '17 Apr 2025', 
            'expired' : '12 Jun 2026',
        },
        {
            'id' : 10,
            'img' : static('app/img/l-10.png'), 
            'title' : 'Front-end Developer',
            'name' : 'Pinterest', 
            'applicants' : '150 Applicants', 
            'class' : 'green', 
            'posted' : '17 Apr 2025', 
            'expired' : '12 Jun 2026',
        }
    ]
    return {"posteds": posteds}


# tables data

def global_tables(request):
    tables = [
        {
            'number' : '01',
            'id' : '1274',
            'name' : 'Basic',
            'type' : 'Job Package',
            'featured' : 'Yes',
            'urgent' : 'Yes',
            'posted' : '04',
            'limit' : '20',
            'duration' : '30',
            'title' : 'Active',
            'class' : 'success',
        },
        {
            'number' : '02',
            'id' : '1285',
            'name' : 'Standard',
            'type' : 'Job Package',
            'featured' : 'Yes',
            'urgent' : 'Yes',
            'posted' : '02',
            'limit' : '25',
            'duration' : '40',
            'title' : 'Expired',
            'class' : 'danger',
        },
        {
            'number' : '03',
            'id' : '1274',
            'name' : 'Platinum',
            'type' : 'Job Package',
            'featured' : 'Yes',
            'urgent' : 'Yes',
            'posted' : '10',
            'limit' : '40',
            'duration' : '75',
            'title' : 'Active',
            'class' : 'success',
        },
        {
            'number' : '04',
            'id' : '6254',
            'name' : 'Standard',
            'type' : 'Job Package',
            'featured' : 'Yes',
            'urgent' : 'Yes',
            'posted' : '07',
            'limit' : '10',
            'duration' : '15',
            'title' : 'Active',
            'class' : 'success',
        },
        {
            'number' : '05',
            'id' : '3256',
            'name' : 'Basic',
            'type' : 'Job Package',
            'featured' : 'Yes',
            'urgent' : 'Yes',
            'posted' : '04',
            'limit' : '20',
            'duration' : '30',
            'title' : 'Expired',
            'class' : 'danger',
        },
        {
            'number' : '06',
            'id' : '4215',
            'name' : 'Basic',
            'type' : 'Job Package',
            'featured' : 'Yes',
            'urgent' : 'Yes',
            'posted' : '04',
            'limit' : '20',
            'duration' : '30',
            'title' : 'Active',
            'class' : 'success',
        },
        {
            'number' : '07',
            'id' : '6254',
            'name' : 'Platinum',
            'type' : 'Job Package',
            'featured' : 'Yes',
            'urgent' : 'Yes',
            'posted' : '04',
            'limit' : '20',
            'duration' : '30',
            'title' : 'Active',
            'class' : 'success',
        }
    ]
    return {"tables": tables}


# teams data

def global_teams(request):
    teams = [
        {
            'img' : static('app/img/team-1.jpg'), 
            'name' : 'Shaurya Preet', 
            'title' : 'Co-Founder',
        },
        {
            'img' : static('app/img/team-2.jpg'), 
            'name' : 'Shivangi Preet', 
            'title' : 'Content Writer',
        },
        {
            'img' : static('app/img/team-3.jpg'), 
            'name' : 'Yash Preet', 
            'title' : 'Content Writer',
        },
        {
            'img' : static('app/img/team-10.jpg'), 
            'name' : 'Calvin English', 
            'title' : 'CEO & Manager',
        },
        {
            'img' : static('app/img/team-5.jpg'), 
            'name' : 'Rahul Gilkrist', 
            'title' : 'App Designer',
        },
        {
            'img' : static('app/img/team-6.jpg'), 
            'name' : 'Adam Wilcard', 
            'title' : 'Web Developer',
        },
        {
            'img' : static('app/img/team-7.jpg'), 
            'name' : 'Adam Wilcard', 
            'title' : 'Web Developer',
        },
        {
            'img' : static('app/img/team-8.jpg'), 
            'name' : 'Adam Wilcard', 
            'title' : 'Web Developer',
        }
    ]
    return {"teams": teams}


# contacts data

def global_contacts(request):
    contacts = [
        {
            'icon' : 'fa-solid fa-location-dot', 
            'name' : 'Hyderabad', 
            'title' : 'Krishe Emerald, Whitefields, Kondapur, Hyderabad, Telangana 500081',
            'mail' : 'shreethemes@gmail.com',
        },
        {
            'icon' : 'fa-solid fa-map-location-dot', 
            'name' : 'Bengaluru', 
            'title' : 'Prestige Cube, Koramangala, Bengaluru, Karnataka 560029',
            'mail' : 'shreethemes@gmail.com',
        },
        {
            'icon' : 'fa-solid fa-map-location', 
            'name' : 'Nagpur', 
            'title' : 'B-101, Vedant Sapphire, Sneha Nagar, Nagpur, Maharashtra, 440015',
            'mail' : 'shreethemes@gmail.com',
        }
    ]
    return {"contacts": contacts}


# buttons data

def global_buttons(request):
    buttons = [
        {
            'class' : 'main',
            'title' : 'Main',
        },
        {
            'class' : 'secondary',
            'title' : 'Secondary',
        },
        {
            'class' : 'success',
            'title' : 'Success',
        },
        {
            'class' : 'danger',
            'title' : 'Danger',
        },
        {
            'class' : 'warning',
            'title' : 'Warning',
        },
        {
            'class' : 'info',
            'title' : 'Info',
        },
        {
            'class' : 'light',
            'title' : 'Light',
        },
        {
            'class' : 'dark',
            'title' : 'Dark',
        },
        {
            'class' : 'red',
            'title' : 'Red',
        },
        {
            'class' : 'green',
            'title' : 'Green',
        },
        {
            'class' : 'light-main',
            'title' : 'Light Main',
        },
        {
            'class' : 'light-red',
            'title' : 'Light Red',
        },
        {
            'class' : 'light-green',
            'title' : 'Light Green',
        },
        {
            'class' : 'outline-main',
            'title' : 'Outline Main',
        },
        {
            'class' : 'outline-red',
            'title' : 'Outline Red',
        },
        {
            'class' : 'outline-green',
            'title' : 'Outline Green',
        },
        {
            'class' : 'outline-dark',
            'title' : 'Outline Dark',
        },
        {
            'class' : 'outline-dark rounded-pill',
            'title' : 'Outline Dark Rounded',
        }
    ]
    return {"buttons": buttons}


# alerts data

def global_alerts(request):
    alerts = [
        {
            'title' : 'main',
        },
        {
            'title' : 'secondary',
        },
        {
            'title' : 'success',
        },
        {
            'title' : 'danger',
        },
        {
            'title' : 'warning',
        },
        {
            'title' : 'info',
        },
        {
            'title' : 'light',
        },
        {
            'title' : 'dark',
        }
    ]
    return {"alerts": alerts}


# links data

def global_links(request):
    links = [
        {
            'title' : 'main',
        },
        {
            'title' : 'secondary',
        },
        {
            'title' : 'success',
        },
        {
            'title' : 'danger',
        },
        {
            'title' : 'warning',
        },
        {
            'title' : 'info',
        },
        {
            'title' : 'light',
        },
        {
            'title' : 'dark',
        }
    ]
    return {"links": links}


# badges data

def global_badges(request):
    badges = [
        {
            'class' : 'bg-main',
            'title' : 'Main',
        },
        {
            'class' : 'text-bg-secondary',
            'title' : 'Secondary',
        },
        {
            'class' : 'text-bg-success',
            'title' : 'Success',
        },
        {
            'class' : 'text-bg-danger',
            'title' : 'Danger',
        },
        {
            'class' : 'text-bg-warning',
            'title' : 'Warning',
        },
        {
            'class' : 'text-bg-info',
            'title' : 'Info',
        },
        {
            'class' : 'text-bg-light',
            'title' : 'Light',
        },
        {
            'class' : 'text-bg-dark',
            'title' : 'Dark',
        },
        {
            'class' : 'badge-md bg-main',
            'title' : 'Main',
        },
        {
            'class' : 'badge-md text-bg-secondary',
            'title' : 'Secondary',
        },
        {
            'class' : 'badge-md text-bg-success',
            'title' : 'Success',
        },
        {
            'class' : 'badge-md text-bg-danger',
            'title' : 'Danger',
        },
        {
            'class' : 'badge-md text-bg-warning',
            'title' : 'Warning',
        },
        {
            'class' : 'badge-md text-bg-info',
            'title' : 'Info',
        },
        {
            'class' : 'badge-md text-bg-light',
            'title' : 'Light',
        },
        {
            'class' : 'badge-md text-bg-dark',
            'title' : 'Dark',
        }
    ]
    return {"badges": badges}


# avatars data

def global_avatars(request):
    avatars = [
        {
            'class' : 'square--80',
        },
        {
            'class' : 'square--70',
        },
        {
            'class' : 'square--50',
        },
        {
            'class' : 'square--30',
        },
        {
            'class' : 'square--20',
        }
    ]
    return {"avatars": avatars}


# infos data

def global_infos(request):
    infos = [
        {
            'title' : 'Company Founder:',
            'name' : 'Mr. Daniel Mark',
        },
        {
            'title' : 'Industry:',
            'name' : 'Technology',
        },
        {
            'title' : 'Founded:',
            'name' : '1997',
        },
        {
            'title' : 'Head Office:',
            'name' : 'London, UK',
        },
        {
            'title' : 'Revenue',
            'name' : '$70B+',
        },
        {
            'title' : 'Company Size:',
            'name' : '20,000+ Emp.',
        },
        {
            'title' : 'Min Exp.',
            'name' : '02 Years',
        },
        {
            'title' : 'Openings',
            'name' : '06 Openings',
        }
    ]
    return {"infos": infos}


# sliders data

def global_sliders(request):
    sliders = [
        {
            'img' : static('app/img/slide-banner-1.jpg'), 
            'title' : 'Real Jobs, Real People, Real Success',
            'desc' : 'The toppings you may chose for that TV dinner pizza slice when you forgot to shop for foods', 
        },
        {
            'img' : static('app/img/slide-banner-2.jpg'), 
            'title' : 'Discover Jobs. Take Action. Win Big.',
            'desc' : 'The toppings you may chose for that TV dinner pizza slice when you forgot to shop for foods', 
        },
        {
            'img' : static('app/img/slide-banner-3.jpg'), 
            'title' : 'Find Work. Build Skills. Grow Fast.',
            'desc' : 'The toppings you may chose for that TV dinner pizza slice when you forgot to shop for foods', 
        },
        {
            'img' : static('app/img/slide-banner-4.jpg'), 
            'title' : 'One Click Closer to Your Next Big Opportunity',
            'desc' : 'The toppings you may chose for that TV dinner pizza slice when you forgot to shop for foods', 
        }
    ]
    return {"sliders": sliders}


def rpo_admin_flag(request):
    """Add `is_rpo_admin` and `is_candidate` booleans to context for templates."""
    user = getattr(request, 'user', None)
    is_rpo = False
    is_candidate = False
    try:
        if user and user.is_authenticated:
            if user.is_superuser:
                is_rpo = True
            else:
                profile = getattr(user, 'profile', None)
                role = getattr(profile, 'role', None) if profile is not None else None
                if role == 'rpo_admin':
                    is_rpo = True
                if role == 'candidate':
                    is_candidate = True
    except Exception:
        is_rpo = False
        is_candidate = False
    return {'is_rpo_admin': is_rpo, 'is_candidate': is_candidate}


def site_config(request):
    """
    Provides site-wide configuration like site name, copyright info.
    """
    return {
        'site_name': 'Jobstock',
        'copyright_year': 2025,
    }