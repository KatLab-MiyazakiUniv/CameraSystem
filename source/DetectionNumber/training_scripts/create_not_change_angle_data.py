import create_data
import train_number_card


def create_not_change_angle_data():
    create_data.create_dataset("train", 1000, is_change_brightness=True, is_change_angle=True)
    create_data.create_dataset("valid", 10, is_change_brightness=True, is_change_angle=True)


if __name__ == '__main__':
    create_not_change_angle_data()
    train_number_card.data_directory = "./"
    train_number_card.main()
