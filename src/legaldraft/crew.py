import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
# Uncomment the following line to use an example of a custom tool
# from legaldraft.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool

search_tool = SerperDevTool(serper_api_key=os.getenv('SERPER_API_KEY'))


mogha_llm = LLM(model='ft:gpt-4o-mini-2024-07-18:synlex-technologies:synlex-draft-s1:AUCRqEhV')
base_llm = LLM(model='ft:gpt-4o-mini-2024-07-18:synlex-technologies:synlex-drafting-mini8:ATQXGQQj')
llm=LLM(model='gpt-4o-mini')
@CrewBase
class Legaldraft():
	"""Legaldraft crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def mogha_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['mogha_agent'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=mogha_llm
		)

	@agent
	def base_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['base_agent'],
			verbose=True,
			llm=base_llm
		)
	
	@agent
	def research_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['research_agent'],
			verbose=True,
			llm=llm,
			tools=[search_tool]	
		)

	@task
	def mogha_task(self) -> Task:
		return Task(
			config=self.tasks_config['mogha_task'],
		)

	@task
	def base_task(self) -> Task:
		return Task(
			config=self.tasks_config['base_task'],
			
		)
	
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_tasks'],
			output_file='report.md',
			expected_output="""A comprehensive legal document that includes:
				1. Thorough legal research findings from Indian law sources
				2. Properly formatted court document following Indian standards
				3. Relevant case laws and statutory references
				4. Jurisdiction-specific compliance details
				5. Complete supporting documentation"""
		)
    
	@crew
	def crew(self) -> Crew:
		"""Creates the Legaldraft crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
