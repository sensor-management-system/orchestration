import { Attachment } from '@/models/Attachment'

describe('Attachment Models', () => {
  test('create a Attachment from an object', () => {
    const attachment = Attachment.createFromObject({ id: 1, url: 'https://foo/test.png', label: 'Testpicture' })
    expect(typeof attachment).toBe('object')
    expect(attachment).toHaveProperty('id', 1)
    expect(attachment).toHaveProperty('url', 'https://foo/test.png')
    expect(attachment).toHaveProperty('label', 'Testpicture')
  })

  it('should set a property by its path', () => {
    const attachment = new Attachment()
    attachment.setPath('id', 1)
    attachment.setPath('url', 'https://foo/test.png')
    attachment.setPath('label', 'Testpicture')

    expect(attachment).toHaveProperty('id', 1)
    expect(attachment).toHaveProperty('url', 'https://foo/test.png')
    expect(attachment).toHaveProperty('label', 'Testpicture')
  })

  it('should throw an error when using a invalid path', () => {
    const attachment = new Attachment()
    expect(() => attachment.setPath('foo', 'bar')).toThrow(TypeError)
  })
})
