from crew import CompanyResearchCrew
import json, sys, csv, argparse
import os
from dotenv import load_dotenv
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from message_generation import generate_outreach_message

# Load environment variables from .env file
load_dotenv()

# Check if API keys are loaded
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY not found in environment variables")
    sys.exit(1)

if not os.getenv("SERPER_API_KEY"):
    print("Warning: SERPER_API_KEY not found in environment variables")

if not os.getenv("GEMINI_API_KEY"):
    print("Warning: GEMINI_API_KEY not found in environment variables")

def research_company(founder_name, company_name):
    """
    Research a single company and its founder
    """
    print(f"Researching {founder_name} of {company_name}...")
    
    try:
        crew_instance = CompanyResearchCrew()
        crew = crew_instance.crew()
        
        # Pass inputs to the kickoff method
        result = crew.kickoff(inputs={
            "founder_name": founder_name,
            "company_name": company_name
        })
        
        # Extract the raw output from each task
        output = {
            "founder_name": founder_name,
            "company_name": company_name,
            "linkedin": crew_instance.linkedin_task.output.raw if hasattr(crew_instance.linkedin_task, 'output') else "Not available",
            "about": crew_instance.company_info_task.output.raw if hasattr(crew_instance.company_info_task, 'output') else "Not available",
            "website": crew_instance.website_task.output.raw if hasattr(crew_instance.website_task, 'output') else "Not available",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return output
    except Exception as e:
        print(f"Error researching {founder_name} of {company_name}: {str(e)}")
        return {
            "founder_name": founder_name,
            "company_name": company_name,
            "linkedin": f"Error: {str(e)}",
            "about": f"Error: {str(e)}",
            "website": f"Error: {str(e)}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
def generate_outreach_message(founder_name, company_name, linkedin, website, about):
        outreach_message = generate_outreach_message(
            founder_name,
            company_name,
            output["linkedin"],
            output["website"],
            output["about"]
        )
        output["outreach_message"] = outreach_message
        return output
"""
def process_csv(csv_file, output_file, max_workers=3):
    
    #Process a CSV file with founder and company information
    
    founders_companies = []
    
    # Read the CSV file
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header row
        
        # Find the founder and company columns
        founder_idx = header.index('Founder Name') if 'Founder Name' in header else 0
        company_idx = header.index('Company Name') if 'Company Name' in header else 1
        
        for row in reader:
            if len(row) > max(founder_idx, company_idx):
                founders_companies.append((row[founder_idx], row[company_idx]))
    
    results = []
    
    # Process in parallel with a limited number of workers
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_founder = {
            executor.submit(research_company, founder, company): (founder, company) 
            for founder, company in founders_companies
        }
        
        for future in as_completed(future_to_founder):
            founder, company = future_to_founder[future]
            try:
                result = future.result()
                results.append(result)
                
                # Save intermediate results to avoid losing data if the process is interrupted
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                
                print(f"Completed research for {founder} of {company}")
            except Exception as e:
                print(f"Error processing {founder} of {company}: {str(e)}")
    
    return results
"""
def main():
    parser = argparse.ArgumentParser(description='Research companies and their founders')
    
    # Create a mutually exclusive group for input methods
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--csv', type=str, help='CSV file with founder and company information')
    input_group.add_argument('--founder', type=str, help='Founder name')
    
    parser.add_argument('--company', type=str, help='Company name (required when using --founder)')
    parser.add_argument('--output', type=str, default='research_results.json', help='Output JSON file')
    parser.add_argument('--workers', type=int, default=3, help='Maximum number of parallel workers')
    
    args = parser.parse_args()
    
    if args.founder and not args.company:
        parser.error("--company is required when using --founder")
    
    if args.csv:
        # Process a CSV file
        results = process_csv(args.csv, args.output, args.workers)
    else:
        # Process a single founder and company
        result = research_company(args.founder, args.company)
        results = [result]
        
        # Save the result to a JSON file
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
    
    print(f"Research completed. Results saved to {args.output}")
    
    # Print a summary of the results
    print("\nSummary:")
    for result in results:
        print(f"- {result['founder_name']} of {result['company_name']}: LinkedIn: {'Found' if result['linkedin'] != 'Not available' else 'Not found'}, Website: {'Found' if result['website'] != 'Not available' else 'Not found'}")

if __name__ == "__main__":
    main()
