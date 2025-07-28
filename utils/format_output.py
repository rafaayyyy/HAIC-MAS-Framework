def format_pydantic_output(output):
    """Format Pydantic output in a user-friendly way"""
    if hasattr(output, 'model_dump'):
        data = output.model_dump()
    elif hasattr(output, 'dict'):
        data = output.dict()
    else:
        return str(output)
    
    def format_dict(d, indent=0):
        """Recursively format dictionary with proper indentation"""
        result = ""
        for key, value in d.items():
            # Format key nicely
            formatted_key = key.replace('_', ' ').title()
            spaces = "  " * indent
            
            if isinstance(value, dict):
                result += f"{spaces} {formatted_key}:\n"
                result += format_dict(value, indent + 1)
            elif isinstance(value, list):
                result += f"{spaces} {formatted_key}:\n"
                for i, item in enumerate(value, 1):
                    if isinstance(item, dict):
                        result += f"{spaces}  {i}. \n"
                        result += format_dict(item, indent + 2)
                    else:
                        result += f"{spaces}  • {item}\n"
            else:
                # Handle long text with line breaks
                if isinstance(value, str) and len(value) > 100:
                    result += f"{spaces} {formatted_key}:\n"
                    # Wrap long text
                    lines = value.split('\n')
                    for line in lines:
                        if line.strip():
                            result += f"{spaces}   {line.strip()}\n"
                else:
                    result += f"{spaces} {formatted_key}: {value}\n"
            result += "\n"
        
        return result
    
    return format_dict(data) 