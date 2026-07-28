// ========================================
// JavaScript Array Methods — Practice File
// Run with: node code-array-methods.js
// ========================================

// --- Sample Data: TechPath Students ---
const students = [
    { name: "Rahul Sharma", age: 22, course: "ADCA", marks: 85, city: "Bhopal" },
    { name: "Priya Patel", age: 20, course: "DCA", marks: 92, city: "Indore" },
    { name: "Amit Kumar", age: 24, course: "ADCA", marks: 67, city: "Delhi" },
    { name: "Sneha Gupta", age: 21, course: "ADCA", marks: 78, city: "Bhopal" },
    { name: "Vikram Singh", age: 23, course: "DCA", marks: 45, city: "Jaipur" },
    { name: "Ananya Reddy", age: 19, course: "ADCA", marks: 95, city: "Hyderabad" },
    { name: "Karan Verma", age: 22, course: "Tally", marks: 58, city: "Bhopal" },
    { name: "Neha Joshi", age: 20, course: "ADCA", marks: 88, city: "Pune" },
];

// --- 1. forEach: Print each student ---
console.log("=== All Students ===");
students.forEach((s, i) => {
    console.log(`${i + 1}. ${s.name} (${s.course}) — ${s.marks} marks`);
});

// --- 2. map: Get just the names ---
const names = students.map(s => s.name);
console.log("\n=== Names Only ===");
console.log(names);

// --- 3. filter: Students who passed (marks >= 60) ---
const passed = students.filter(s => s.marks >= 60);
console.log("\n=== Passed Students (60+) ===");
passed.forEach(s => console.log(`  ${s.name}: ${s.marks}`));

// --- 4. filter: Failed students ---
const failed = students.filter(s => s.marks < 60);
console.log("\n=== Failed Students ===");
failed.forEach(s => console.log(`  ${s.name}: ${s.marks}`));

// --- 5. find: First student from Bhopal ---
const bhopalStudent = students.find(s => s.city === "Bhopal");
console.log("\n=== First Bhopal Student ===");
console.log(`  ${bhopalStudent.name} — ${bhopalStudent.course}`);

// --- 6. filter + map: Names of ADCA students ---
const adcaNames = students
    .filter(s => s.course === "ADCA")
    .map(s => s.name);
console.log("\n=== ADCA Student Names ===");
console.log(adcaNames);

// --- 7. reduce: Total marks ---
const totalMarks = students.reduce((sum, s) => sum + s.marks, 0);
const avgMarks = totalMarks / students.length;
console.log("\n=== Marks Stats ===");
console.log(`  Total: ${totalMarks}`);
console.log(`  Average: ${avgMarks.toFixed(1)}`);

// --- 8. sort: By marks (highest first) ---
const toppers = [...students].sort((a, b) => b.marks - a.marks);
console.log("\n=== Ranked by Marks ===");
toppers.forEach((s, i) => {
    console.log(`  ${i + 1}. ${s.name} — ${s.marks}`);
});

// --- 9. some + every ---
const anyFailed = students.some(s => s.marks < 60);
const allPassed = students.every(s => s.marks >= 60);
console.log("\n=== Checks ===");
console.log(`  Anyone failed? ${anyFailed}`);
console.log(`  Everyone passed? ${allPassed}`);

// --- 10. reduce: Count students per course ---
const courseCount = students.reduce((counts, s) => {
    counts[s.course] = (counts[s.course] || 0) + 1;
    return counts;
}, {});
console.log("\n=== Students per Course ===");
console.log(courseCount);

// --- 11. Chaining: Top 3 ADCA students ---
const top3ADCA = students
    .filter(s => s.course === "ADCA")
    .sort((a, b) => b.marks - a.marks)
    .slice(0, 3)
    .map(s => `${s.name} (${s.marks})`);
console.log("\n=== Top 3 ADCA Students ===");
console.log(top3ADCA);

// --- 12. Real-world: Generate result cards ---
console.log("\n=== Result Cards ===");
students.forEach(s => {
    const grade = s.marks >= 90 ? "A+" :
                  s.marks >= 75 ? "A" :
                  s.marks >= 60 ? "B" :
                  s.marks >= 40 ? "C" : "F";
    const status = s.marks >= 60 ? "PASS" : "FAIL";
    console.log(`  ${s.name} | ${s.course} | ${s.marks}/100 | Grade: ${grade} | ${status}`);
});
