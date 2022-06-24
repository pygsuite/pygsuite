from enum import Enum


class QuestionType(Enum):
    ROW_QUESTION = "rowQuestion"
    FILE_UPLOAD_QUESTION = "fileUploadQuestion"
    TIME_QUESTION = "timeQuestion"
    DATE_QUESTION = "dateQuestion"
    SCALE_QUESTION = "scaleQuestion"
    TEXT_QUESTION = "textQuestion"
    CHOICE_QUESTION = "choiceQuestion"

    @classmethod
    def _missing_(cls, value):
        from pygsuite.forms.generated.text_question import TextQuestion
        from pygsuite.forms.generated.date_question import DateQuestion

        if isinstance(value, TextQuestion):
            return QuestionType.TEXT_QUESTION
        elif isinstance(value, DateQuestion):
            return QuestionType.DATE_QUESTION


class GoToAction(Enum):
    GO_TO_ACTION_UNSPECIFIED = "GO_TO_ACTION_UNSPECIFIED"
    NEXT_SECTION = "NEXT_SECTION"
    RESTART_FORM = "RESTART_FORM"
    SUBMIT_FORM = "SUBMIT_FORM"


class ItemType(Enum):
    QUESTION_ITEM = "questionItem"
    QUESTION_GROUP_ITEM = "questionGroupItem"
    PAGE_BREAK_ITEM = "pageBreakItem"
    TEXT_ITEM = "textItem"
    IMAGE_ITEM = "imageItem"
    VIDEO_ITEM = "videoItem"

    @classmethod
    def _missing_(cls, value):
        from pygsuite.forms.generated.page_break_item import PageBreakItem
        from pygsuite.forms.generated.question_item import QuestionItem
        from pygsuite.forms.generated.question_group_item import QuestionGroupItem
        from pygsuite.forms.generated.text_item import TextItem
        from pygsuite.forms.generated.video_item import VideoItem
        from pygsuite.forms.generated.image_item import ImageItem

        if isinstance(value, PageBreakItem):
            return cls.PAGE_BREAK_ITEM
        elif isinstance(value, QuestionItem):
            return cls.QUESTION_ITEM
        elif isinstance(value, QuestionGroupItem):
            return cls.QUESTION_GROUP_ITEM
        elif isinstance(value, TextItem):
            return cls.TEXT_ITEM
        elif isinstance(value, VideoItem):
            return cls.VIDEO_ITEM
        elif isinstance(value, ImageItem):
            return cls.IMAGE_ITEM
