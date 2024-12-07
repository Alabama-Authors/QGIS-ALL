function extractEducationKeywords(bio) {
    const educationKeywords = ["education", "attended", "lecturer", "honors", "taught", "professor", "teacher"];
    const alabamaUniversities = [
        "Air University", "Alabama A&M University", "Alabama College of Osteopathic Medicine", "Alabama State University",
        "Amridge University", "Athens State University", "Auburn University", "Auburn University at Montgomery",
        "Bevill State Community College", "Birmingham School of Law", "Bishop State Community College", "Calhoun Community College",
        "Central Alabama Community College", "Chattahoochee Valley Community College", "Coastal Alabama Community College",
        "Columbia Southern University", "Community College of the Air Force", "Enterprise State Community College", "Faulkner University",
        "Gadsden State Community College", "H. Councill Trenholm State Community College", "Heritage Christian University", "Highlands College",
        "Huntingdon College", "Huntsville Bible College", "J.F. Drake State Community and Technical College", "J. F. Ingram State Technical College",
        "Jacksonville State University", "Jefferson State Community College", "Lawson State Community College", "Lurleen B. Wallace Community College",
        "Marion Military Institute", "Miles College", "Miles Law School", "Northeast Alabama Community College", "Northwest–Shoals Community College",
        "Oakwood University", "Reid State Technical College", "Samford University", "Selma University", "Shelton State Community College",
        "Snead State Community College", "Southern Union State Community College", "Spring Hill College", "Stillman College", "Talladega College",
        "Troy University", "Tuskegee University", "United States Sports Academy", "University of Alabama", "University of Alabama at Birmingham",
        "University of Alabama in Huntsville", "University of Mobile", "University of Montevallo", "University of North Alabama", "University of South Alabama",
        "University of West Alabama", "Wallace Community College", "Wallace Community College Selma", "Wallace State Community College Columbia College Missouri",
        "Edward Via College of Osteopathic Medicine", "Embry-Riddle Aeronautical University", "Florida Institute of Technology", "Southeastern University",
        "United States Army Command and General Staff College", "Alabama Presbyterian College", "Birmingham–Southern College", "Concordia College Alabama",
        "Daniel Payne College", "Judson College", "Southeastern Bible College", "Southern Benedictine College", "Virginia College"
    ];

    // Create a regular expression pattern that matches any of the education keywords followed by 0-5 words of any characters
    const keywordPattern = new RegExp("\\b(" + educationKeywords.join("|") + ")\\b(\\s[A-Za-z]+){0,5}", "gi");
    // Create a regular expression pattern that matches any of the Alabama universities followed by 0-5 words of any characters
    const universityPattern = new RegExp("\\b(" + alabamaUniversities.join("|") + ")\\b(\\s[A-Za-z]+){0,5}", "gi");

    const educationMatches = bio.match(keywordPattern) || [];
    const universityMatches = bio.match(universityPattern) || [];

    const results = [...new Set([...educationMatches, ...universityMatches])];

    if (results.includes("education")) {
        results.splice(results.indexOf("education"), 1);
        results.unshift("education");
    }

    return results.join(", ");
}