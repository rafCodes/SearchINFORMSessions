import re
import pdfplumber

# Function to divide the document into sections based on "Summit - XXX"
def divide_sections(text):
    sections = re.split('(Summit - )', text)
    # Combine the Summit title with the following text into a single section
    # return [''.join(sections[i:i+2]) for i in range(0, len(sections)-1, 2)]
    return sections

# Function to filter sections that contain one or more of the given words
def filter_sections_by_keywords(sections, keywords):
    keyword_pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in keywords) + r')\b', re.IGNORECASE)
    return [section for section in sections if keyword_pattern.search(section)]

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path, pageCountStart, pageCountEnd):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ''
        count = 0
        for page in pdf.pages:
            count += 1
            if count <= pageCountStart:
                continue
            full_text += page.extract_text()
            print(count)
            if count == pageCountEnd:
                return full_text
        return full_text

# Function to save filtered sections to a markdown file with a table of contents
def save_to_markdown_with_toc(sections, output_file):
    toc = []
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write the Table of Contents
        f.write("# Table of Contents\n\n")
        for i, section in enumerate(sections):
            splitSection = section.split("\n")
            title = splitSection[1]
            toc_item = f"{i+1}. [{title}](#{title.lower().replace(' ', '-')})"
            toc.append(toc_item)
        f.write("\n".join(toc) + "\n\n")

        # Write each section with markdown formatting
        for section in sections:
            splitSection = section.split("\n")
            roomNumber = splitSection[0]
            title = splitSection[1]
            f.write(f"## {title}\n\n")
            f.write(f"Room: {roomNumber}\n\n")
            f.write(f"{section.strip()}\n\n")
            f.write(f"{'-' * 80}\n\n")

# Function to save filtered sections to a markdown file
def save_to_markdown(sections, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for section in sections:
            # Write each section with markdown formatting
            f.write(f"## {section.strip()}\n\n")
            f.write(f"{'-' * 80}\n\n")

# Example usage
if __name__ == "__main__":
    print("code is active")
    # Step 1: Extract text from the PDF
    pdf_path = 'Program Book 10-18.pdf'  # Replace with the path to your PDF file
    pageCountStart = 137
    pageCountEnd = 208
    document_text = extract_text_from_pdf(pdf_path)
    print("Got text")

    # Step 2: Divide the document into sections
    sections = divide_sections(document_text)
    print("Divided text")

    # Step 3: List of keywords to search for
    keywords = ['my keyword']  # Add more keywords as needed
    
    # Step 4: Filter sections by keywords
    filtered_sections = filter_sections_by_keywords(sections, keywords)

    # Step 5: Save the filtered sections as markdown to a file
    output_file = 'filtered_sections.md'  # Replace with your desired output file name
    save_to_markdown_with_toc(filtered_sections, output_file)

    print(f"Filtered sections saved to {output_file}")