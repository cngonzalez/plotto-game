import click
from plotto_gen import PlottoGen

__author__ = "Carolina Gonzalez"
plotto = PlottoGen()

# @click.group()
# def main():
#     """
#     Simple CLI for illustrating a very basic story generation strategy
#     """
#     pass

@click.command()
# @click.argument('feeling')
def start():
    click.echo("GAME START")
    click.echo("=====================")
    terminal = False
    while not terminal:
        feelings = plotto.get_next_feelings()
        print_step(feelings)
        feeling = int(click.prompt("How do you feel about this? Choose a number")) - 1
        return_feeling(feelings, feeling)
        plotto.advance_with_feeling(feeling)
        terminal = plotto.determine_terminal()
        if terminal:
            click.echo(plotto.get_current_state())

    click.echo("GAME OVER!")
    click.echo("I HOPE YOU ENJOYED PLAYING :) GOODBYE")

def return_feeling(feelings, feeling):
    click.echo("=====================")
    click.echo(f"You chose {feeling + 1}: {feelings[feeling]}")
    click.echo("=====================")

def print_step(feelings):
    click.echo(plotto.get_current_state())
    click.echo("=====================")
    click.echo("This may make you feel:")
    for idx, feeling in enumerate(feelings):
        click.echo(f"{idx+1}. {feeling}")
    click.echo("=====================")

if __name__ == "__main__":
    start()
