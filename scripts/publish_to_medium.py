import requests
import json
import os
import yaml
from datetime import datetime

class Medium:
    def __init__(self, token):
        self.token = token
        self.user_id = self._get_user_id()
        self.banner_image_url = ""
        self.canonical_url = "https://www.faizanbashir.me/"

    def set_banner_image_url(self, image_path):
        self.banner_image_url = self.get_base_url() + image_path

    def get_banner_image_url(self):
        return self.banner_image_url

    def set_canonical_url(self, url):
        self.canonical_url = url

    def get_canonical_url(self):
        return self.canonical_url

    def get_base_url(self):
        base_url = "https://www.faizanbashir.me/"
        return base_url

    def add_watermark(self, content, filename):
        base_url = self.get_base_url()
    
        filename_without_extension = filename.replace('.md', '')
        
        split_position = [i for i, c in enumerate(filename_without_extension) if c == '-'][2]
        
        # date_part = filename_without_extension[:split_position]
        article_title_part = filename_without_extension[split_position + 1:]
        
        article_url = f"{base_url}{article_title_part}"

        self.set_canonical_url(article_url)

        banner = f"![Banner Image]({self.get_banner_image_url()})\n\n"
        
        watermark = f"\n\nYou can read this and other articles at **[faizanbashir.me]({article_url})**"
        return banner + content + watermark

    def _get_user_id(self):
        """Private method to get the Medium user ID using the API token."""
        try:
            url = "https://api.medium.com/v1/me"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()["data"]["id"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user ID: {e}")
            return None
    
    def _post_article(self, title, content, content_format, tags, publish_status):
        """Private method to handle posting the article to Medium."""
        if not self.user_id:
            print("User ID is missing. Cannot post article.")
            return
        
        try:
            url = f"https://api.medium.com/v1/users/{self.user_id}/posts"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            data = {
                "title": title,
                "contentFormat": content_format,
                "content": content,
                "tags": tags if tags else [],
                "publishStatus": publish_status,
                "license": "all-rights-reserved",
                "notifyFollowers": True,
                "canonicalUrl": self.get_canonical_url()
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise HTTPError for bad responses
            
            result = response.json()
            print(f"Successfully posted: {title}")
            print(f"View it at: {result['data']['url']}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"Failed to post article: {e}")
            return None

    def _get_drafts(self):
        """Private method to retrieve all drafts from Medium."""
        if not self.user_id:
            print("User ID is missing. Cannot retrieve drafts.")
            return
        
        try:
            url = f"https://api.medium.com/v1/users/{self.user_id}/posts?status=draft"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            drafts = response.json()["data"]
            return drafts
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve drafts: {e}")
            return None

    def save_as_draft(self, title, content, content_format="markdown", tags=None):
        """Public method to save an article as a draft on Medium."""
        print("Saving article as a draft...")
        return self._post_article(title, content, content_format, tags, publish_status="draft")

    def publish_to_medium(self, title, content, content_format="markdown", tags=None):
        """Public method to publish an article directly to Medium."""
        print("Publishing article to Medium...")
        return self._post_article(title, content, content_format, tags, publish_status="public")
    
    def publish_draft(self, draft_id):
        """Public method to publish an existing saved draft on Medium."""
        print(f"Publishing draft with ID: {draft_id}...")
        
        try:
            url = f"https://api.medium.com/v1/posts/{draft_id}"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            data = {
                "publishStatus": "public",
            }
            response = requests.put(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            
            result = response.json()
            print(f"Draft successfully published: {result['data']['title']}")
            print(f"View it at: {result['data']['url']}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"Failed to publish draft: {e}")
            return None

    def process_code_blocks(self, content):
        """Replaces highlight blocks with appropriate code block tags"""

        processed_content = content
        while True:
            start_tag = "{% highlight"
            end_tag = "{% endhighlight %}"

            start_index = processed_content.find(start_tag)
            if start_index == -1:
                break  # No more highlight blocks found

            end_index = processed_content.find(end_tag, start_index) + len(end_tag)
            if end_index == -1:
                print("Error: Unmatched highlight block")
                break 

            code_block = processed_content[start_index:end_index]

            # Extract language more robustly using regex
            import re
            match = re.search(r"{% highlight (\w+) %}", code_block)
            if match:
                language = match.group(1)
            else:
                print("Error: Could not extract language from highlight block")
                language = ""  # Set a default or handle the error as needed

            code_content = code_block[code_block.find('\n') + 1: code_block.rfind('\n')]

            replacement = f"```{language.lower()}\n{code_content}\n```" 
            processed_content = processed_content.replace(code_block, replacement)

        return processed_content

    def extract_metadata_and_content(self, filepath):
        """Extracts title, tags, and content from a .md file"""

        try:
            with open(filepath, 'r') as file:
                content = file.read()

            # Find the first two '---' delimiters
            delimiter_count = 0
            start_index = 0
            end_index = 0
            for i in range(len(content)):
                if content[i:i+3] == '---':
                    delimiter_count += 1
                    if delimiter_count == 1:
                        start_index = i + 3  # Start after the first delimiter
                    elif delimiter_count == 2:
                        end_index = i  # End at the second delimiter
                        break

            if end_index <= start_index:
                print(f"Error: First two delimiters not found or invalid in {filepath}")
                return None

            frontmatter = content[start_index:end_index].strip()
            try:
                metadata = yaml.safe_load(frontmatter)
                title = metadata.get('title')
                tags = metadata.get('tags')
                image = metadata.get('cover')

                if not title or not tags or not image:
                    print(f"Error: Missing 'title' or 'tags' or 'cover' in frontmatter of {filepath}")
                    return None
                
                if image:
                    self.set_banner_image_url(image)

            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {filepath}: {e}")
                return None

            # Find the second '---' delimiter for content extraction
            delimiter_count = 0
            content_start_index = 0
            for i in range(end_index, len(content)):
                if content[i:i+3] == '---':
                    delimiter_count += 1
                    if delimiter_count == 1:
                        content_start_index = i + 3
                        break

            if content_start_index == 0:
                print(f"Error: Second content delimiter not found in {filepath}")
                return None
            
            extracted_content = content[content_start_index:].strip()
            processed_content = self.process_code_blocks(extracted_content)

            extracted_content = content[content_start_index:].strip()
            return {
                'title': title,
                'tags': tags,
                'content': self.add_watermark(processed_content, filepath)
            }

        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
            return None
        except IOError as e:
            print(f"Error reading file {filepath}: {e}")
            return None

# Example usage (remains the same)

# Example usage
if __name__ == "__main__":
    medium_token = "26c2a1e46777e3c6bfefe582d9b3c00e80725f23b08dd1a5f32d8a427a096fc8a"
    medium_client = Medium(medium_token)
    directory_path = '../_posts/terraform/'  # Replace with your directory path

    for filename in os.listdir(directory_path):
        article_tags = []
        if filename.endswith(".md"):
            filepath = os.path.join(directory_path, filename)
            result = medium_client.extract_metadata_and_content(filepath)
            if result:
                print(f"Data from {filename}:")
                print(f"  Title: {result['title']}")
                article_tags = result['tags']
                article_tags.append('Programming')
                print(f"  Tags: {article_tags}")
                print(f"  Content: {result['content'][:50]}")
                
                draft_response = medium_client.save_as_draft(result['title'], result['content'], tags=article_tags)
                if draft_response:
                    print(draft_response)

    # article_tags = ["Python", "Programming", "Tech"]  # Optional

    # Save as draft
    # draft_response = medium_client.save_as_draft(article_title, article_content, tags=article_tags)
    
    # if draft_response:
    #     draft_id = draft_response['data']['id']

    #     # Publish the saved draft
    #     medium_client.publish_draft(draft_id)
