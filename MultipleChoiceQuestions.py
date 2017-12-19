from Tkinter import *
import pickle

playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
for player in playerData:
    if player[2] == 1:
        playerName = player[0]

class MultipleChoiceQuestions:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiple Choice Questions")

        self.score = 0
        self.questionNumber = 0

        self.questions = [ "1. What is the largest planet in the solar system?",
                           "2. Which planet has the moon Io orbiting it?",
                           "3. By which process does the Sun produce its energy?",
                           "4. This planet has a longer day than year.",
                           "5. Which spacecraft has made it into interstellar space?",
                           "6. What celestial body is responsible for the Earth's changing tides?",
                           "7. Which of these planets does NOT have rings?",
                           "8. How many satellites does Mars have?",
                           "9. Who was the first American in space?",
                           "10. Which of these have less power than the Apollo lander's computer?",]

        self.options = [["Saturn", "Jupiter", "The Sun", "Pluto"],
                        ["Neptune", "Earth", "Saturn", "Jupiter"],
                        ["nuclear fission", "nuclear fusion", "photosynthesis", "chemosynthesis"],
                        ["Venus", "Pluto", "Neptune", "Mars"],
                        ["Cassini", "Voyager II", "Rosetta", "Voyager I"],
                        ["The Moon", "The Sun", "Mars", "The Milky Way"],
                        ["Jupiter", "Saturn", "Uranus", "Mars"],
                        ["1", "16", "2", "8"],
                        ["Neil Armstrong", "Alan Shepard", "Buzz Aldrin", "Yuri Gagarin"],
                        ["a smartphone", "a washing machine", "a calculator", "None of these"]]

        self.correctAnswers = ["b", "d", "b", "a", "d", "a", "d", "c", "b", "d"]

        self.questionLabel = Label(self.root, text=self.questions[self.questionNumber], width=100, font=100)
        self.questionLabel.grid(row=1, columnspan=4)

        Label(self.root, text="a.", font=100).grid(row=2, column=0)
        Label(self.root, text="b.", font=100).grid(row=2, column=2)
        Label(self.root, text="c.", font=100).grid(row=3, column=0)
        Label(self.root, text="d.", font=100).grid(row=3, column=2)

        self.option1 = Label(self.root, text=self.options[self.questionNumber][0], width=20, font=100)
        self.option2 = Label(self.root, text=self.options[self.questionNumber][1], width=20, font=100)
        self.option3 = Label(self.root, text=self.options[self.questionNumber][2], width=20, font=100)
        self.option4 = Label(self.root, text=self.options[self.questionNumber][3], width=20, font=100)

        self.option1.grid(row=2, column=1)
        self.option2.grid(row=2, column=3)
        self.option3.grid(row=3, column=1)
        self.option4.grid(row=3, column=3)

        self.feedbackLabel = Label(self.root, text="")
        self.feedbackLabel.grid(row=4, columnspan=4)
        self.answerInput = Entry(self.root)
        self.answerInput.grid(row=5, columnspan=4)
        Button(self.root, text="Submit Answer", command=self.submit_answer).grid(row=6, columnspan=4)
        Button(self.root, text="QUIT", command=self.quit_game).grid(row=7, columnspan=4)

    def submit_answer(self):
        answer = str(self.answerInput.get())
        if answer == self.correctAnswers[self.questionNumber]:
            self.score += 100
            if self.questionNumber < len(self.questions) - 1:
                self.questionNumber += 1
            self.questionLabel.config(text=self.questions[self.questionNumber])
            self.option1.config(text=self.options[self.questionNumber][0])
            self.option2.config(text=self.options[self.questionNumber][1])
            self.option3.config(text=self.options[self.questionNumber][2])
            self.option4.config(text=self.options[self.questionNumber][3])
            self.answerInput.delete(0, END)
        else:
            self.feedbackLabel.config(text="Incorrect answer")

    def quit_game(self):
        global playerName
        try:
            playerData = pickle.load(open("data/leaderboard.txt", 'rb'))
            for player in playeData:
                if player[0] == playerName:
                    player[1] += self.score
            pickle.dump(playerData, open("data/leaderboard.txt", 'wb'))
        except:
            pass
        quit()

root = Tk()
MCQ = MultipleChoiceQuestions(root)

root.mainloop()
