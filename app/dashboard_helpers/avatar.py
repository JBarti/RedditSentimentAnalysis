def avatar(image_url: str, name: str, occupation: str, size: int = 80):
    """
    Render a circular avatar with name and occupation in Streamlit.
    
    Args:
        image_url (str): URL or local path to your avatar image
        name (str): Person's name
        occupation (str): Occupation or title
        size (int): Diameter of the avatar image in pixels
    """
    
    return f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 10px;
    ">
        <img src="{image_url}" 
             style="
                 width: {size}px;
                 height: {size}px;
                 border-radius: 50%;
                 object-fit: cover;
             "
        >
        <div style="display: flex; flex-direction: column;">
            <span style="font-weight: bold; font-size: 18px;">{name}</span>
            <span style="font-size: 14px; color: gray;">{occupation}</span>
        </div>
    </div>
    """
