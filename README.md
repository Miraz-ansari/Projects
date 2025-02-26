# Projects
### **What Are We Trying to Do?** 🤔  

We are **automating the evaluation of insurance documents** to decide whether an insurance submission should be **Approved** or **Declined** based on fleet mileage calculations.  

---

### **Step-by-Step Explanation:**
1. **Extract Data from Insurance Documents 📄**  
   - We take **PDF files** containing insurance details (fleet size, mileage, etc.).
   - We use **Python** to read and extract important information.

2. **Perform Mileage Calculations 📊**  
   - We calculate **PPT (Per Person Trip)** using mileage formulas:
     - **If Annual Mileage is given** → `PPT = Annual Mileage / 15,000`
     - **If only Reimbursed Mileage is given** → `PPT = Reimbursed Mileage / (Rate * 15,000)`
     - Different states (e.g., Oregon & Washington) use a **higher reimbursement rate**.

3. **Make an Approval Decision ✅❌**  
   - If **Total Fleet > Calculated PPT**, the insurance submission is **Approved**.
   - Otherwise, it is **Declined**.

4. **Validate with AI 🤖**  
   - We use **AI (GPT-4)** to **double-check our calculations**.
   - AI follows the same rules and compares its decision with our manual result.
   - If AI agrees → ✅ **Correct**  
   - If AI disagrees → ❌ **Needs review**

---

### **Why Are We Doing This?** 🎯  
- **Automate Manual Work** → No need for humans to review documents manually.  
- **Ensure Accuracy** → AI cross-checks calculations.  
- **Faster Decision-Making** → Insurance companies can process applications quickly.  

Would you like a **flowchart or diagram** to visualize this? 🚀

Here's a **visual flowchart** explaining the entire process of our automated insurance evaluation system. I'll generate it now. 🚀

Here's the **flowchart** illustrating our automated insurance evaluation process. 🚀  

This diagram visually explains how the system:  
✅ Extracts data from PDFs  
✅ Performs calculations  
✅ Makes approval decisions  
✅ Validates with AI  
✅ Compares AI vs. Manual decision  

Let me know if you need any modifications or additional explanations! 📊
