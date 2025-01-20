export interface Label {
    id: number
    label: string
    color: string
}

export enum TaskCompleted {
    today = 'today',
    always = 'always',
    never = 'never'
}

/**
 * 
 * title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_tasks"
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assigned_tasks"
    )

    labels = models.ManyToManyField(Labels, related_name="tasks")

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="tasks")
    checked = models.BooleanField(default=False)
 */
export interface Task {
    id: number | null
    created_at: number
    title: string
    description: string
    due_date: string
    created_by: number
    assigned_to: number
    labels: Label[]
    client: {
        id: number
        socialreasonorname: string
        client_number: string
    },
    checked: boolean
}