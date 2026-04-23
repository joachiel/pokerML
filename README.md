# pokerML

ML to play online poker

Good — memory and CLAUDE.md are set. Now the discussions you asked about:

Which ML approach?
Your chess comparison is a good instinct, but poker has one big fundamental difference: hidden information. In chess both players see the whole board. In poker you can't see your opponent's hole cards, which means classic MCTS/AlphaZero doesn't apply directly.

Here are the main paths:

Reinforcement Learning (PPO / DQN)
The approach you're thinking of — agent takes actions, receives reward (chips won/lost), learns a policy. Easier to get started, lots of libraries (Stable-Baselines3, RLlib), and produces satisfying "watch it learn" training curves. The downside is that in imperfect information games, a naive RL agent learns to exploit the specific opponents it trained against, not a generally strong strategy. It can be beaten by someone who plays differently.

Counterfactual Regret Minimization (CFR)
This is the gold standard specifically for poker — it's what Libratus and Pluribus (the superhuman poker AIs) are built on. It computes a Nash equilibrium strategy, meaning it converges to a strategy that can't be exploited no matter what opponents do. The tradeoff: it's a poker-specific algorithm, more complex to implement, and the math is less "general ML" and more game theory. Less flashy on a portfolio to someone who doesn't know poker AI.

My suggestion: Start with PPO via self-play. It's the most recognizable ML approach, produces clear training curves (which look great on a portfolio), and will get you to a working bot faster. If you get deep into the project, CFR is the "correct" thing and would genuinely impress someone who knows the domain.

What makes a good GitHub project for employers?
Roughly in order of impact:

Immediately visible (first 30 seconds)

A README with a clear one-line description, a demo (even a GIF of the bot playing), and a quick-start command
A clean commit history with meaningful messages (not "fix stuff", "wip")
A working CI badge (GitHub Actions running your tests on every push — takes ~20 minutes to set up)
Shows engineering discipline

requirements.txt or pyproject.toml — project should be reproducible
Tests with reasonable coverage, especially for the evaluator (easy to write, important to get right)
Type hints on function signatures — makes code readable without comments
Consistent formatting (just pick black and run it)
Shows you understand ML

A training curve plot in the README showing the agent improving over time — this is the single most compelling thing for this specific project
Evaluation against a random agent as a baseline
A brief explanation in the README of why you chose your approach (shows you thought about it)
GitHub workflow hygiene

Use Issues to track the bugs and features — even if you're solo, it shows you work like a team
Use branches (git checkout -b fix/ace-ranking) and PRs, even merging into your own main — it creates a visible contribution graph and shows you know the workflow
A changelog or milestone markers
What not to over-invest in early: fancy project boards, wikis, or extensive docs. Employers mostly want to see: does it work, does it have tests, does the ML actually learn something.

The order I'd tackle things: fix the evaluator bugs → add proper action interface → write proper tests → set up CI → then start on the agent. That way the foundation is solid before ML complexity is layered on top.
