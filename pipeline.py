from agents import writer_chain, critic_chain
from tools import search_web, scrape_url
import re


def extract_first_url(text: str):

    urls = re.findall(r'https?://\S+', text)

    return urls[0] if urls else None


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # STEP 1 - SEARCH TOOL
    print("\n" + "=" * 50)
    print("STEP 1 - SEARCH TOOL WORKING...")
    print("=" * 50)

    search_result = search_web.invoke(topic)

    state["search_results"] = search_result

    print("\nSEARCH RESULT:\n", state["search_results"])

    # STEP 2 - URL EXTRACTION + SCRAPING
    print("\n" + "=" * 50)
    print("STEP 2 - SCRAPING TOP RESOURCE...")
    print("=" * 50)

    url = extract_first_url(state["search_results"])

    if url:

        print(f"\nURL FOUND: {url}")

        scraped_content = scrape_url.invoke(url)

        state["scraped_content"] = scraped_content

    else:

        state["scraped_content"] = "No URL found to scrape."

    print("\nSCRAPED CONTENT:\n", state["scraped_content"][:2000])

    # STEP 3 - WRITER CHAIN
    print("\n" + "=" * 50)
    print("STEP 3 - WRITER IS DRAFTING THE REPORT...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFINAL REPORT:\n", state["report"])

    # STEP 4 - CRITIC REPORT
    print("\n" + "=" * 50)
    print("STEP 4 - CRITIC IS REVIEWING THE REPORT...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCRITIC REPORT:\n", state["feedback"])

    return state


if __name__ == "__main__":

    topic = input("\nEnter a research topic: ")

    run_research_pipeline(topic)