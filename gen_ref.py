from yaml import load, Loader
from watchdog.observers import Observer
from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
import sys
import time
import pathlib
import sched

scheduled_event = None

scheduler = sched.scheduler(time.monotonic, time.sleep)

class ChangeHandler(FileSystemEventHandler):
	def __init__(self, fn):
		self.fn = fn

	def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
		global scheduled_event
		if scheduled_event != None:
			scheduler.cancel(scheduled_event)
		scheduled_event = scheduler.enter(1, 1, self.fn)
		scheduler.run()

class MarkdownBuilder:
	def __init__(self):
		self.builder = []
	
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
		with open(filepath, "w", newline="\n") as f:
			first = True
			for s in self.builder:
				if first:
					first = False
				else:
					f.write("\n\n")
				f.write(s)

class RefArg:
	def __init__(self, arg_yaml):
		self.name = arg_yaml["name"]
		self.arg_type = arg_yaml["type"]
		self.desc = arg_yaml["desc"]
		self.fn = ("fn" in arg_yaml) and arg_yaml["fn"]

class MarkdownRefAndMeta:
	def __init__(self, markdown: str, name: str, ret: str, stack: str, args: list[RefArg]):
		self.markdown = markdown
		self.name = name
		self.ret = ret
		self.stack = stack
		self.args = args

def read_markdown_file_and_metadata(filepath: str):
	yaml_lines = []
	md_lines = []

	looking_for_metadata = True
	reading_metadata = False
	with open(filepath, "r") as f:
		lines = f.readlines()
		for line in lines:
			if looking_for_metadata:
				if line.startswith("---"):
					looking_for_metadata = False
					reading_metadata = True
			elif reading_metadata:
				if line.startswith("---"):
					reading_metadata = False
				else:
					yaml_lines.append(line)
			else:
				md_lines.append(line)
	
	meta = load("\n".join(yaml_lines), Loader=Loader)
	
	return MarkdownRefAndMeta(
		markdown="".join(md_lines),
		name=meta["name"],
		ret=meta["ret"],
		stack=meta["stack"],
		args=list(map(lambda a: RefArg(a), meta["args"])) if meta["args"] is not None else list(),
	)

def build_signature(meta: MarkdownRefAndMeta):
	args = ""
	if len(meta.args) > 0:
		args = ", ".join(map(lambda arg: arg.arg_type if arg.fn else arg.arg_type + " " + arg.name, meta.args))
	return f"{meta.ret} {meta.name}({args})"

def gen():
	global scheduled_event
	scheduled_event = None

	builder = MarkdownBuilder()

	with open("./ref/_ref.yaml") as ref_stream:
		data = load(ref_stream, Loader=Loader)
		if data == None:
			print("No data")
			return
		builder.append_h1(data["title"])
		sections = data["sections"]
		first_section = True
		for section in sections:
			if first_section:
				first_section = False
			else:
				builder.append("----\n")
			builder.append_h2(section["name"])
			first_fn = True
			for md_filepath in section["functions"]:
				if first_fn:
					first_fn = False
				else:
					builder.append("----\n")
				meta = read_markdown_file_and_metadata(f"ref/{md_filepath}")
				builder.append_subsection(meta.name)
				builder.append_signature(build_signature(meta), meta.stack)
				if len(meta.args) > 0:
					builder.append("\n".join(map(lambda arg: f"- `{arg.name}`: {arg.desc}", meta.args)))
				builder.append(meta.markdown)
	
	builder.write("docs/reference.md")

	print("Generated")

def watch_and_gen():
	event_handler = ChangeHandler(gen)
	observer = Observer()
	observer.schedule(event_handler, "./ref", recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	finally:
		observer.stop()
		observer.join()

def main():
	if len(sys.argv) > 1 and sys.argv[1] == "-w":
		gen()
		watch_and_gen()
	else:
		gen()

if __name__ == "__main__":
	main()
