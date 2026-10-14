"""Demo for Extension 3: Thank-you speech."""
from story import TalentShow, ThankYouSpeech, audition


def main():
    speech = ThankYouSpeech("Marcus")
    print("Normal case: describe() ->", speech.describe())
    print("Normal case: duration() ->", speech.duration())

    show = TalentShow("Marcus", 2)
    print("Booked successfully:", show.book(speech))
    print("Minutes left after booking:", show.clock.remaining)

    empty_show = TalentShow("Marcus", 0)
    print("Refused case:", empty_show.book(speech))
    print("Remaining after refusal:", empty_show.clock.remaining)

    print("All speeches in the lineup:")
    audition([speech])


if __name__ == "__main__":
    main()
