import tkinter as tk  # import tkinter for gui
from tkinter import messagebox  # import messagebox for pop-up messages
import requests  # import requests to make api calls

# define the main app class
class RecipeScraperApp:
    def __init__(self, root):
        self.root = root  # set the root window
        self.root.title("Recipe Scraper & Meal Planner")  # set the window title
        self.root.geometry("750x750")  # set the window size
        self.root.configure(bg="#f0f8ff")  # set the background color

        # add a title label at the top of the window
        title = tk.Label(
            self.root,
            text="Recipe Scraper & Meal Planner",
            font=("Arial", 22, "bold"),
            bg="#f0f8ff",
            fg="#2a9d8f"
        )
        title.pack(pady=20)  # add padding around the title

        # create a frame for the search method selection
        method_frame = tk.Frame(self.root, bg="#f0f8ff")
        method_frame.pack(pady=10)

        self.search_method = tk.StringVar(value="ingredients")  # default to ingredients

        # radio button for searching by ingredients
        tk.Radiobutton(
            method_frame,
            text="Search by Ingredients",
            variable=self.search_method,
            value="ingredients",
            bg="#f0f8ff",
            font=("Arial", 12),
            command=self.update_placeholder
        ).grid(row=0, column=0, padx=10)

        # radio button for searching by recipe name
        tk.Radiobutton(
            method_frame,
            text="Search by Recipe Name",
            variable=self.search_method,
            value="recipe_name",
            bg="#f0f8ff",
            font=("Arial", 12),
            command=self.update_placeholder
        ).grid(row=0, column=1, padx=10)

        # create a frame for the user input section
        input_frame = tk.Frame(self.root, bg="#f0f8ff")
        input_frame.pack(pady=20)

        # label to prompt the user for input
        self.input_label = tk.Label(
            input_frame,
            text="Enter Ingredients (comma-separated):",
            font=("Arial", 12),
            bg="#f0f8ff"
        )
        self.input_label.grid(row=0, column=0, padx=5)

        # entry box for user input
        self.search_entry = tk.Entry(input_frame, width=50)
        self.search_entry.grid(row=0, column=1, padx=5)

        # button to initiate the search
        search_button = tk.Button(input_frame, text="Search", command=self.search_recipes, bg="#2a9d8f", fg="white")
        search_button.grid(row=0, column=2, padx=10)

        # label to display results summary
        self.results_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f0f8ff")
        self.results_label.pack(pady=10)

        # frame to display the search results
        self.results_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.results_frame.pack(pady=10)

    def update_placeholder(self):
        # update the input label and placeholder based on the selected search method
        if self.search_method.get() == "ingredients":
            self.input_label.config(text="Enter Ingredients (comma-separated):")
            self.search_entry.delete(0, tk.END)  # clear the input box
        else:
            self.input_label.config(text="Enter Recipe Name:")
            self.search_entry.delete(0, tk.END)  # clear the input box

    def search_recipes(self):
        # get the user's input from the entry box
        query = self.search_entry.get().strip()
        if not query:  # check if the input is empty
            messagebox.showerror("Error", "Please enter a search term!")
            return

        self.results_label.config(text="Fetching recipes...")  # update the results label
        self.results_frame.destroy()  # clear the previous results
        self.results_frame = tk.Frame(self.root, bg="#f0f8ff")  # recreate the results frame
        self.results_frame.pack(pady=10)

        # spoonacular api key and url
        API_KEY = "475fceb561ae425eaeb57237e8a4366a"  # replace with your spoonacular api key
        if self.search_method.get() == "ingredients":
            # construct the API URL for ingredients
            url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={query}&number=10&apiKey={API_KEY}"
        else:
            # construct the API URL for recipe name
            url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&number=10&apiKey={API_KEY}"

        try:
            # make a get request to the API
            response = requests.get(url)
            response.raise_for_status()  # raise an exception for HTTP errors
            recipes = response.json()["results"] if self.search_method.get() == "recipe_name" else response.json()

            if not recipes:  # check if no recipes are found
                self.results_label.config(text="No recipes found. Try a different search.")
                return

            # update the results label
            self.results_label.config(text=f"Recipes for '{query}':")
            for recipe in recipes:
                title = recipe["title"]
                link = f"https://spoonacular.com/recipes/{title.replace(' ', '-').lower()}-{recipe['id']}"

                # create a frame for each recipe
                recipe_frame = tk.Frame(self.results_frame, bg="#f0f8ff")
                recipe_frame.pack(anchor="w", pady=5, padx=10)

                # label to display the recipe title
                recipe_label = tk.Label(
                    recipe_frame, text=title, font=("Arial", 12, "bold"),
                    bg="#f0f8ff", fg="#264653", cursor="hand2"
                )
                recipe_label.pack(anchor="w")
                recipe_label.bind("<Button-1>", lambda e, link=link: self.open_link(link))

        except requests.exceptions.RequestException as e:  # handle exceptions
            self.results_label.config(text="Error fetching recipes. Please try again.")
            messagebox.showerror("Error", str(e))

    @staticmethod
    def open_link(link):
        import webbrowser  # import webbrowser to open links
        webbrowser.open(link)  # open the given link in the default browser

# run the application
if __name__ == "__main__":
    root = tk.Tk()  # create the main tkinter window
    app = RecipeScraperApp(root)  # initialize the app
    root.mainloop()  # run the tkinter event loop
