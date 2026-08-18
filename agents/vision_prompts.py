from langchain_core.prompts import PromptTemplate

# Prompt for describing what's in a chart/image
VISION_DESCRIBE_PROMPT = PromptTemplate.from_template(
    "You are analyzing a chart or image extracted from a document. "
    "Describe what type of chart it is (bar, line, pie, etc.), "
    "what data it shows, and any clear trends. "
    "Be factual — only describe what is visibly present.\n\n"
    "Image context: {image_context}\n\n"
    "Description:"
)

# Prompt for answering a specific question about a chart
VISION_QA_PROMPT = PromptTemplate.from_template(
    "You are analyzing a chart image to answer a question. "
    "Only use information visibly shown in the chart. "
    "If the answer cannot be determined from the chart, say so clearly.\n\n"
    "Chart context: {image_context}\n\n"
    "Question: {question}\n\n"
    "Answer:"
)

if __name__ == "__main__":
    # Simulated chart context 
    sample_chart_context = (
        "Bar chart titled 'Monthly Sales'. X-axis shows months Jan-May. "
        "Y-axis shows Units Sold (0-200). Bars increase from Jan (120) to May (200), "
        "with a dip in April (140)."
    )

    print("=== Describe prompt ===")
    print(VISION_DESCRIBE_PROMPT.format(image_context=sample_chart_context))

    print("\n=== QA prompt ===")
    print(VISION_QA_PROMPT.format(
        image_context=sample_chart_context,
        question="Which month had the highest sales?"
    ))