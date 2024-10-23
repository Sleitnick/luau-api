from yaml import load, Loader

class MarkdownBuilder:
	builder = []
	
	def append(self, text: str):
		self.builder.append(text)
	
	def append_h1(self, text: str):
		self.builder.append("# " + text)
	
	def append_h2(self, text: str):
		self.builder.append("## " + text)
	
	def append_h3(self, text: str):
		self.builder.append("### " + text)
	
	def append_subsection(self, text: str):
		self.builder.append(f"### <span class=\"subsection\">`{text}`</span>")
	
	def append_signature(self, sig: str, stack: str):
		self.builder.append(f"<span class=\"signature\">`{sig}`</span>\n<span class=\"stack\">`[{stack}]`</span>")
	
	def write(self, filepath: str):
		with open(filepath, "w") as f:
			first = True
			for s in self.builder:
				if first:
					first = False
				else:
					f.write("\n\n")
				f.write(s)

def build_signature(fn):
	args = ", ".join(map(lambda arg: arg["type"] + " " + arg["name"], fn["args"]))
	return fn["ret"] + " " + fn["name"] + "(" + args + ")"

def main():
	builder = MarkdownBuilder()

	builder.append_h1("Luau C API Reference")

	with open("ref.yaml") as ref_stream:
		data = load(ref_stream, Loader=Loader)
		sections = data["sections"]
		for section in sections:
			builder.append_h2(section["name"])
			for fn in section["functions"]:
				builder.append_subsection(fn["name"])
				builder.append_signature(build_signature(fn), fn["stack"])
				builder.append("\n".join(map(lambda arg: "- `" + arg["name"] + "`: " + arg["desc"], fn["args"])))
				builder.append(fn["desc"])
	
	builder.write("docs/reference.md")

	print("Generated")

if __name__ == "__main__":
	main()
