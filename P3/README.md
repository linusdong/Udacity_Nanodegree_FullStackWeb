# Item Catalog: Getting Started

## Change log
* April 21st 2015, initial commit. Readme file added.

## Project description
In this project, you will be developing a web application that provides a list of items within a variety of categories and integrate third party user registration and authentication. Authenticated users should have the ability to post, edit, and delete their own items.

You will be creating this project essentially from scratch, no templates have been provided for you. This means that you have free reign over the HTML, the CSS, and the files that include the application itself utilizing Flask.

There are four parts that you will need to complete:
* the HTML (structure of the pages)
* the CSS (the style of the pages)
* the Flask Application (to put it online) it must include authentication/authorization to allow users to login before making changes
* the database (to store and organize the information)

### Additional Functionality
In addition to the basic functions listed above, this project has many opportunities to go above and beyond what is required. Some ways to achieve exceeds specifications are to include the following requirements:

1. API Endpoints: Research and implement additional API endpoints, such as RSS, Atom, or XML. While we do require at the bare minimum a JSON endpoint, we encourage you to research and implement a different endpoint to see what else is out there.

2. CRUD: Read: Add an item image field that is read from the database and displayed on the page. This project is being built from scratch meaning that the information that you include and the layout of the page are entirely up to you. Add pictures for a more vibrant web application!

3. CRUD: Create: Update the new item form to correctly process the inclusion of item images. If you included additional information to include images, there should be a way to include those images when entering in new items into the database.

4. CRUD: Update: Update the edit/update item form to correctly process the inclusion of item images. Again, to stay consistent with the inclusion of images, items that already exist should have the option of changing the image as well.

5. CRUD: Delete: Research and implement this function using POST requests and nonces to prevent cross-site request forgeries (CSRF).

6. Comments: Comments are not just a way for you to keep track of what you’re writing in terms of code, but also a great way to help other developers who may be reading your code. While comment preferences may differ from team to team, the general idea is that good comments cover the main purpose of the code, mention inputs and outputs, etc. Check out the comments section of PEP-8 and the Google Python Style Guide to get a better idea of good comments.

## How to use the project

1. Install Vagrant and VirtualBox if you have not done so already. Instructions on how to do so can be found on the websites as well as in the course materials.

2. Clone the fullstack-nanodegree-vm repository. There is a catalog folder provided for you, but no files have been included. If a catalog folder does not exist, simply create your own inside of the vagrant folder.

3. Launch the Vagrant VM (by typing vagrant up in the directory fullstack/vagrant from the terminal). You can find further instructions on how to do so here.

4. Write the Flask application locally in the /vagrant/catalog directory (which will automatically be synced to /vagrant/catalog within the VM). Name it application.py.

5. Run your application within the VM by typing python /vagrant/catalog/application.py into the Terminal. If you named the file from step 4 as something other than application.py, in the above command substitute in the file name on your computer.

6. Access and test your application by visiting http://localhost:8000 locally on your browser.

## Project grading guideline
![Project grading guideline](./pics/project3rubric.png)
