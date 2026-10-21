"""A2 checks for refused and successful strict bookings.

Run from the repository root with:
    py -3 stories/05_campus_talent_show/demo_marcus_s25b13_032.py
"""
from story import (
    Dance,
    ShowChoiceError,
    ShowRequestError,
    ShowResourceError,
    StrictTalentShow,
)


class NegativeDurationChoice:
    name = "Negative-duration test choice"

    def duration(self):
        return -1


def state(show):
    return show.clock.remaining, show.act_count


def check_attempt(label, show, choice, expected_error=None, expected_result=None):
    before = state(show)
    actual_error = None
    actual_result = None

    print(f"\n{label}")
    print(f"Before: {before[0]} minutes; {before[1]} booked acts")
    try:
        actual_result = show.safe_book(choice)
    except ShowChoiceError as error:
        actual_error = error
        print(f"Actual: ShowChoiceError: {error}")
    except ShowRequestError as error:
        actual_error = error
        print(f"Actual: ShowRequestError: {error}")
    except ShowResourceError as error:
        actual_error = error
        print(f"Actual: ShowResourceError: {error}")
    finally:
        print("Attempt completed.")

    after = state(show)
    if expected_error is not None:
        assert isinstance(actual_error, expected_error), (
            f"Expected {expected_error.__name__}, got "
            f"{type(actual_error).__name__ if actual_error else 'no error'}"
        )
        assert after == before, f"A refused booking changed state: {before} -> {after}"
        print(f"Expected: {expected_error.__name__}; state unchanged: {after}")
    else:
        assert actual_error is None, f"Unexpected error: {actual_error}"
        assert actual_result == expected_result, (
            f"Expected booking result {expected_result!r}, got {actual_result!r}"
        )
        print(f"Expected: {expected_result}")
        print(f"After: {after[0]} minutes; {after[1]} booked acts")


def main():
    print("=== MARCUS AINEBYONA: A2 STRICT BOOKING CHECKS ===")

    check_attempt(
        "Missing choice: expect ShowChoiceError and no state change.",
        StrictTalentShow("Marcus", 5),
        None,
        expected_error=ShowChoiceError,
    )
    check_attempt(
        "Negative duration: expect ShowRequestError and no state change.",
        StrictTalentShow("Marcus", 5),
        NegativeDurationChoice(),
        expected_error=ShowRequestError,
    )
    check_attempt(
        "Unaffordable act: expect ShowResourceError and no state change.",
        StrictTalentShow("Marcus", 5),
        Dance("Long set", minutes=6),
        expected_error=ShowResourceError,
    )

    successful_show = StrictTalentShow("Marcus", 5)
    check_attempt(
        "Affordable act: expect a successful booking and updated state.",
        successful_show,
        Dance("Short set", minutes=3),
        expected_result="MC Marcus books Short set dance.",
    )
    assert state(successful_show) == (2, 1)
    print("Success check passed: 2 minutes remain and 1 act was booked.")


if __name__ == "__main__":
    main()