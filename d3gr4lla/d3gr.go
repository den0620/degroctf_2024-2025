package main

import (
	"fmt"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// Model represents the application state
type Model struct {
	currentDrink   map[string]int
	selectedIngr   int
	mode           Mode
	textInput      textinput.Model
	clientRequest  string
	message        string
	secretRecipe   map[string]int
	servedCorrect  bool
	windowWidth    int
	windowHeight   int
	ingredientList []string
	totalUsed      int
	maxIngredients int
}

// Mode represents the current application mode
type Mode int

const (
	Normal Mode = iota
	Shaking
	Serving
	Result
)

var (
	focusedStyle  = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))
	blurredStyle  = lipgloss.NewStyle().Foreground(lipgloss.Color("240"))
	titleStyle    = lipgloss.NewStyle().Foreground(lipgloss.Color("39")).Bold(true)
	itemStyle     = lipgloss.NewStyle().PaddingLeft(4)
	selectedStyle = lipgloss.NewStyle().PaddingLeft(2).Foreground(lipgloss.Color("170"))
	clientStyle   = lipgloss.NewStyle().Foreground(lipgloss.Color("39")).Bold(true).Italic(true).PaddingTop(1)
	shakeStyle    = lipgloss.NewStyle().Foreground(lipgloss.Color("226")).Bold(true)
	resultStyle   = lipgloss.NewStyle().Foreground(lipgloss.Color("82")).Bold(true)
	errorStyle    = lipgloss.NewStyle().Foreground(lipgloss.Color("196")).Bold(true)
	actionStyle   = lipgloss.NewStyle().Foreground(lipgloss.Color("213")).Bold(true)
)

func initialModel() Model {
	ingredients := []string{
		"Adelhyde RUSH",
		"Plan B: Cfe",
		"Monstew Deltergy",
		"Flanersh Nrg",
		"Kared Bulline",
		"*shaker*", // This is now an action, not an ingredient
	}

	currentDrink := make(map[string]int)
	for _, ingr := range ingredients[:5] { // Only the first 5 are ingredients
		currentDrink[ingr] = 0
	}

	// Secret recipe is the flag - needs to be decoded
	secretRecipe := map[string]int{
		"Adelhyde RUSH":    4,
		"Plan B: Cfe":      0,
		"Monstew Deltergy": 1,
		"Flanersh Nrg":     0,
		"Kared Bulline":    5,
	}

	ti := textinput.New()
	ti.Placeholder = "Serve the drink? (y/n)"
	ti.CharLimit = 1
	ti.Width = 21

	return Model{
		currentDrink:   currentDrink,
		selectedIngr:   0,
		mode:           Normal,
		textInput:      ti,
		clientRequest:  "I need something that'll help me pass my math exams...",
		secretRecipe:   secretRecipe,
		servedCorrect:  false,
		ingredientList: ingredients,
		totalUsed:      0,
		maxIngredients: 10,
	}
}

func (m Model) Init() tea.Cmd {
	return textinput.Blink
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit

		case "up", "w":
			if m.mode == Normal {
				m.selectedIngr = max(0, m.selectedIngr-1)
			}

		case "down", "s":
			if m.mode == Normal {
				m.selectedIngr = min(len(m.ingredientList)-1, m.selectedIngr+1)
			}

		case "left", "a":
			if m.mode == Normal && m.selectedIngr < len(m.ingredientList)-1 { // Not the shaker
				ingr := m.ingredientList[m.selectedIngr]
				if m.currentDrink[ingr] > 0 {
					m.currentDrink[ingr]--
					m.totalUsed--
				}
			}

		case "right", "d":
			if m.mode == Normal && m.selectedIngr < len(m.ingredientList)-1 { // Not the shaker
				ingr := m.ingredientList[m.selectedIngr]
				if m.currentDrink[ingr] < 10 && m.totalUsed < m.maxIngredients {
					m.currentDrink[ingr]++
					m.totalUsed++
				}
			}

		case "enter", " ":
			if m.mode == Normal {
				if m.selectedIngr == len(m.ingredientList)-1 { // Shaker selected
					if m.totalUsed > 0 {
						m.mode = Shaking
						return m, tea.Tick(time.Second, func(_ time.Time) tea.Msg {
							return shakeFinishedMsg{}
						})
					}
				}
			} else if m.mode == Serving {
				m.textInput, cmd = m.textInput.Update(msg)
				
				// Process serving decision
				if m.textInput.Value() == "y" || m.textInput.Value() == "Y" {
					m.mode = Result
					m.textInput.Blur()
					
					// Check if the recipe matches
					correct := true
					for k, v := range m.secretRecipe {
						if m.currentDrink[k] != v {
							correct = false
							break
						}
					}
					
					if correct {
						m.servedCorrect = true
						magicbytes := []byte{
							0x64, 0x65, 0x67, 0x72, 0x6f, 0x5f, 0x79, 0x6b, 0x5f, 0x77, 0x6f,
							0x5f, 0x74, 0x68, 0x65, 0x79, 0x5f, 0x64, 0x6f, 0x5f, 0x32, 0x5f,
							0x67, 0x75, 0x79, 0x73, 0x5f, 0x6c, 0x69, 0x6b, 0x65, 0x5f, 0x75,
							0x73, 0x5f, 0x69, 0x6e, 0x5f, 0x73, 0x33, 0x73, 0x63,
						}
						m.message = "Perfect! " + string(magicbytes)
					} else {
						m.message = "That's not what I wanted!"
					}
				} else if m.textInput.Value() == "n" || m.textInput.Value() == "N" {
					m.mode = Normal
					m.textInput.Blur()
				}
			} else if m.mode == Result {
				// Reset the drink
				for k := range m.currentDrink {
					m.currentDrink[k] = 0
				}
				m.totalUsed = 0
				m.mode = Normal
				m.message = ""
			}
		}

	case tea.WindowSizeMsg:
		m.windowWidth = msg.Width
		m.windowHeight = msg.Height
		
	case shakeFinishedMsg:
		m.mode = Serving
		m.textInput.Focus()
		return m, textinput.Blink
	}

	if m.mode == Serving {
		m.textInput, cmd = m.textInput.Update(msg)
	}

	return m, cmd
}

// Custom message for shake animation completion
type shakeFinishedMsg struct{}

func (m Model) View() string {
	var s strings.Builder
	
	// Title
	title := titleStyle.Render("D3GR 4LL-A: Uwutism Action")
	s.WriteString(title + "\n\n")
	
	// Client request
	clientRequest := clientStyle.Render("ninefid: \"" + m.clientRequest + "\"")
	s.WriteString(clientRequest + "\n\n")
	
	// Current drink
	s.WriteString("Current Mix: " + fmt.Sprintf("[%d/%d ingredients]\n", m.totalUsed, m.maxIngredients))

	// Column widths for alignment
	ingrWidth := 20
	barWidth := 10
	amountWidth := 5
	
	// Header line
	headerLine := fmt.Sprintf("  %-*s %-*s %-*s", ingrWidth, "Ingredient", barWidth, "Amount", amountWidth, "Qty")
	s.WriteString(headerLine + "\n")
	s.WriteString("  " + strings.Repeat("-", ingrWidth+barWidth+amountWidth) + "\n")
	
	// Ingredients
	for i, ingr := range m.ingredientList {
		var line string
		
		if i < len(m.ingredientList)-1 { // Regular ingredients
			amount := m.currentDrink[ingr]
			amountStr := strings.Repeat("█", amount) + strings.Repeat("░", 10-amount)
			
			if i == m.selectedIngr && m.mode == Normal {
				line = selectedStyle.Render(fmt.Sprintf(">  %-*s %-*s [%*d]", 
					ingrWidth-1, ingr, 
					barWidth, amountStr, 
					amountWidth-3, amount))
			} else {
				line = itemStyle.Render(fmt.Sprintf("%-*s %-*s [%*d]", 
					ingrWidth, ingr, 
					barWidth, amountStr, 
					amountWidth-3, amount))
			}
		} else { // Shaker button
			if i == m.selectedIngr && m.mode == Normal {
				line = actionStyle.Render(fmt.Sprintf("> %-*s", ingrWidth+barWidth+amountWidth-2, ingr))
			} else {
				line = actionStyle.Render(fmt.Sprintf("  %-*s", ingrWidth+barWidth+amountWidth-2, ingr))
			}
		}
		
		s.WriteString(line + "\n")
	}
	
	// Instructions
	s.WriteString("\n")
	s.WriteString("Controls: ↑/↓ to select, ←/→ to adjust amount, Enter to use shaker\n\n")
	
	// Status messages
	if m.mode == Shaking {
		s.WriteString(shakeStyle.Render("*Shaking the drink vigorously*\n"))
	} else if m.mode == Serving {
		s.WriteString("Serve the drink to the client?\n")
		s.WriteString(m.textInput.View() + "\n")
	} else if m.mode == Result {
		if m.servedCorrect {
			s.WriteString(resultStyle.Render(m.message) + "\n")
		} else {
			s.WriteString(errorStyle.Render(m.message) + "\n")
		}
		s.WriteString("\nPress Enter to mix a new drink\n")
	}
	
	return s.String()
}

func main() {
	p := tea.NewProgram(initialModel(), tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Error running program: %v", err)
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
