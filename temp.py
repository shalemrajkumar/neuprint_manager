import inquirer
choices=['Computers', 'Books', 'Science', 'Nature', 'Fantasy', 'History']
questions = [ inquirer.Checkbox('interests', message="What are you interested in?",choices = choices,),]
answers = inquirer.prompt(questions)
print(answers)
print(answers['interests'])
