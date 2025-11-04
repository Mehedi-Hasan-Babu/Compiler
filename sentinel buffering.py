EOF = "EOF"  # sentinel symbol

class TwoBufferInput:
    def __init__(self, text, buffer_size=5):
        self.buffer_size = buffer_size
        self.buffers = [[], []]
        self.text = text
        self.pos = 0
        self.active_buffer = 0
        self.forward = 0

        # Load only the first buffer
        self.load_buffer(0)

    def load_buffer(self, index):
        """Load buffer[index] with sentinel at the end."""
        start = self.pos
        end = min(self.pos + self.buffer_size, len(self.text))
        chunk = list(self.text[start:end])
        self.pos = end
        chunk.append(EOF)
        self.buffers[index] = chunk
        print(f"Buffer[{index}] loaded: {chunk}")

    def get_next_char(self):
        char = self.buffers[self.active_buffer][self.forward]
        self.forward += 1

        if char == EOF:
            if self.pos < len(self.text):
                # Switch buffer
                old_buffer = self.active_buffer
                self.active_buffer = 1 - self.active_buffer
                self.forward = 0
                self.load_buffer(self.active_buffer)
                print(f"[Switch] End of buffer[{old_buffer}] → switch to buffer[{self.active_buffer}]")
                # Read next char from new buffer
                return self.get_next_char()
            else:
                return None  # True EOF
        else:
            return char


# ----------------------
# Example Usage
# ----------------------
text = "hello world!"
print(text , "\n")
scanner = TwoBufferInput(text, buffer_size=5)

print("\nCharacters read with sentinel buffering:\n")
while True:
    ch = scanner.get_next_char()
    if ch is None:
        print("\n[END] All characters processed.")
        break
    print(f"Read: {ch}")
