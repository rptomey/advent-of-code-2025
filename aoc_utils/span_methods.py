def merge_spans(spans):
    """
    Helper function for combining an iterable number of spans/ranges into a simplified iterable based on finding overlaps.
    
    :param spans: An iterable (list or set) containing tuples representing ranges of integers `(low, high)`
    """
    # Sort the spans by their lowest number
    sorted_spans = sorted(spans, key=lambda x: x[0])

    # Set for holding new merged spans built from span overlap
    merged_spans = set()

    # Initialize span comparison with the first one in the list
    current_start, current_end = sorted_spans[0]

    # For all remaining spans, check for overlap
    for span in sorted_spans[1:]:
        next_start, next_end = span
        if next_start <= (current_end + 1):
            # Keep building the merged span
            current_end = max(current_end, next_end)
        else:
            # Save the merged span and start the next one
            merged_spans.add((current_start, current_end))
            current_start, current_end = next_start, next_end
    
    # When we run out of spans to compare, we still have one waiting to be saved
    merged_spans.add((current_start, current_end))

    # Send back the simplified set of merged spans
    return merged_spans