class KernelException(Exception):
    """
    Represents exception returned by the kernel, 
    mostly used to return errors in the boot sub-
    module.

    @param reason is the reason for the failure 
    """

    def __init__(self, reasons, *args: object) -> None:
        super().__init__(*args)